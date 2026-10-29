// ========================================
// FILE: auth_repository.dart
// MÔ TẢ: Repository duy nhất cho Authentication - Tuân thủ Clean Architecture
// QUAN TRỌNG: File duy nhất được phép import Firebase!
// ========================================
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../../../core/config/users-role.dart';
import '../../../domain/models/user_model.dart';

// ========================================
// CLASS: AuthRepository
// MÔ TẢ: Repository duy nhất cho Authentication - Clean Architecture
// ========================================
class AuthRepository {
  static AuthRepository? _instance;
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  AuthRepository._internal();

  static AuthRepository defaultClient() {
    _instance ??= AuthRepository._internal();
    return _instance!;
  }

  // ========================================
  // GETTER: currentUserModel - Trả về UserModel thay vì Firebase User
  // ========================================
  Future<UserModel?> get currentUserModel async {
    final firebaseUser = _auth.currentUser;
    if (firebaseUser == null) return null;

    try {
      // Query bằng email vì document ID có thể khác với Firebase Auth UID
      final userQuery = await _firestore
          .collection('users')
          .where('email', isEqualTo: firebaseUser.email)
          .limit(1)
          .get();

      if (userQuery.docs.isEmpty) return null;

      return UserModel.fromFirestore(userQuery.docs.first);
    } catch (e) {
      print('DEBUG: ❌ Error getting currentUserModel: $e');
      return null;
    }
  }

  // ========================================
  // HÀM: signInWithEmailAndPassword - Trả về UserModel
  // MÔ TẢ: Đăng nhập tối ưu và trả về UserModel (gộp từ signInWithRole)
  // ========================================
  Future<UserModel> signInWithEmailAndPassword(
      String email, String password) async {
    try {
      print("🔐 Đang xác thực: $email");

      // 1. Đăng nhập Firebase Auth
      final credential = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Đăng nhập thất bại: Không nhận được thông tin user');
      }

      print("✅ Auth thành công, đang lấy user data...");

      // 2. Tìm UserModel từ Firestore bằng email (vì doc ID có thể khác với Firebase Auth UID)
      final userQuery = await _firestore
          .collection('users')
          .where('email', isEqualTo: email)
          .limit(1)
          .get();

      if (userQuery.docs.isEmpty) {
        throw Exception('User không tồn tại trong hệ thống');
      }

      final userDoc = userQuery.docs.first;
      final firebaseAuthUid = credential.user!.uid;

      // 3. Đồng bộ UID: Cập nhật document với Firebase Auth UID nếu chưa có
      final docData = userDoc.data();
      if (docData['firebaseAuthUid'] != firebaseAuthUid) {
        await _firestore.collection('users').doc(userDoc.id).update({
          'firebaseAuthUid': firebaseAuthUid,
          'lastLoginAtLocal': DateTime.now().toString(),
        });
      } else {
        // Chỉ cập nhật lastLoginAt nếu UID đã đồng bộ
        _firestore.collection('users').doc(userDoc.id).update({
          'lastLoginAtLocal': DateTime.now().toString(),
        }).catchError(
            (e) => print('Warning: Could not update lastLoginAt: $e'));
      }

      final roleFromFirestore = userDoc.data()?['role'];
      print("✅ Đăng nhập hoàn tất - Role từ Firestore: $roleFromFirestore");

      final userModel = UserModel.fromFirestore(userDoc);
      print(
          "✅ UserModel parsed - Role: ${userModel.role.name}, UID: ${userModel.uid}");

      return userModel;
    } catch (e) {
      print("❌ Lỗi đăng nhập: $e");
      throw Exception('Đăng nhập thất bại: $e');
    }
  }

  // ========================================
  // HÀM: signInWithUsernameAndPassword
  // MÔ TẢ: Đăng nhập bằng username/password (không phụ thuộc email)
  // ========================================
  Future<UserModel> signInWithUsernameAndPassword(
    String username,
    String password,
  ) async {
    final normalizedUsername = username.trim().toLowerCase();

    // 1. Map username -> email (ưu tiên cấu hình cục bộ để không cần truy vấn trước khi auth)
    final email = await _resolveEmailForUsername(normalizedUsername);
    if (email == null) {
      throw Exception('Tài khoản không tồn tại hoặc chưa được cấu hình');
    }

    // 2. Xử lý password: nếu là "admin" (5 ký tự) thì chuyển thành "admin1" (6 ký tự) để đáp ứng yêu cầu Firebase
    String normalizedPassword = password.trim();
    if (normalizedPassword == 'admin' && normalizedUsername == 'admin') {
      normalizedPassword = 'admin1';
    }

    // 3. Đăng nhập FirebaseAuth bằng email để lấy token hợp lệ
    return signInWithEmailAndPassword(email, normalizedPassword);
  }

  // ========================================
  // HÀM: createUserAccount - Trả về UserModel
  // MÔ TẢ: Đăng ký tài khoản mới và trả về UserModel
  // ========================================
  Future<UserModel> createUserAccount(
    String name,
    String email,
    String password,
    UserRole role,
  ) async {
    try {
      // 1. Tạo Firebase Auth user
      final credential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Đăng ký thất bại: Không tạo được tài khoản');
      }

      // 2. Cập nhật displayName
      await credential.user!.updateDisplayName(name);

      // 3. Tạo UserModel
      final userModel = UserModel(
        uid: credential.user!.uid,
        email: email,
        name: name,
        displayName: name,
        role: role,
        photoUrl: null,
        createdAt: DateTime.now(),
        lastLoginAt: null,
        settings: const UserSettings(), // Default settings
        isActive: true,
        isDefault: false,
      );

      // 4. Lưu UserModel vào Firestore
      await _firestore
          .collection('users')
          .doc(credential.user!.uid)
          .set(userModel.toFirestore());

      return userModel;
    } catch (e) {
      throw Exception('Đăng ký thất bại: $e');
    }
  }

  // ========================================
  // HÀM: signOut
  // MÔ TẢ: Đăng xuất người dùng
  // ========================================
  Future<void> signOut() async {
    try {
      await _auth.signOut();
    } catch (e) {
      throw Exception('Đăng xuất thất bại: $e');
    }
  }

  // ========================================
  // HÀM: sendPasswordResetEmail
  // MÔ TẢ: Gửi email đặt lại mật khẩu
  // ========================================
  Future<void> sendPasswordResetEmail(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } catch (e) {
      throw Exception('Gửi email đặt lại mật khẩu thất bại: $e');
    }
  }

  // ========================================
  // HÀM: getUserById - Trả về UserModel
  // MÔ TẢ: Lấy thông tin user theo uid, trả về UserModel
  // ========================================
  Future<UserModel?> getUserById(String uid) async {
    try {
      final doc = await _firestore.collection('users').doc(uid).get();
      if (!doc.exists) return null;

      return UserModel.fromFirestore(doc);
    } catch (e) {
      return null;
    }
  }

  // ========================================
  // HÀM: updateUserProfile - Nhận UserModel
  // MÔ TẢ: Cập nhật thông tin user bằng UserModel
  // ========================================
  Future<UserModel> updateUserProfile(UserModel updatedUser) async {
    try {
      await _firestore
          .collection('users')
          .doc(updatedUser.uid)
          .update(updatedUser.toFirestore());

      // Trả về UserModel sau khi cập nhật
      return updatedUser;
    } catch (e) {
      throw Exception('Cập nhật thông tin thất bại: $e');
    }
  }

  // ========================================
  // HÀM: checkUserSession - Trả về UserModel
  // MÔ TẢ: Kiểm tra session hiện tại và trả về UserModel
  // ========================================
  Future<UserModel?> checkUserSession() async {
    try {
      final firebaseUser = _auth.currentUser;
      if (firebaseUser == null) return null;

      // Kiểm tra user document trong Firestore
      final userDoc =
          await _firestore.collection('users').doc(firebaseUser.uid).get();
      if (!userDoc.exists) return null;

      return UserModel.fromFirestore(userDoc);
    } catch (e) {
      return null;
    }
  }

  // ========================================
  // STREAM: userModelStream - Stream UserModel thay vì Firebase User
  // MÔ TẢ: Stream theo dõi thay đổi auth state, trả về UserModel
  // ========================================
  Stream<UserModel?> get userModelStream {
    return _auth.authStateChanges().asyncMap((firebaseUser) async {
      if (firebaseUser == null) return null;

      try {
        final userDoc =
            await _firestore.collection('users').doc(firebaseUser.uid).get();
        if (!userDoc.exists) return null;

        return UserModel.fromFirestore(userDoc);
      } catch (e) {
        return null;
      }
    });
  }

  // ========================================
  // HÀM: signInAnonymously - Cho testing
  // MÔ TẢ: Đăng nhập ẩn danh cho việc test
  // ========================================
  Future<User?> signInAnonymously() async {
    try {
      final credential = await _auth.signInAnonymously();
      return credential.user;
    } catch (e) {
      throw Exception('Đăng nhập ẩn danh thất bại: $e');
    }
  }

  // ========================================
  // GETTER: isUserLoggedIn
  // MÔ TẢ: Kiểm tra nhanh có user đang đăng nhập không
  // ========================================
  bool get isUserLoggedIn => _auth.currentUser != null;

  // ========================================
  // METHOD: getCurrentUserId
  // MÔ TẢ: Lấy user ID hiện tại (cho CourseRepository)
  // ========================================
  Future<String?> getCurrentUserId() async {
    // Thử lấy từ Firebase Auth trước
    final firebaseUser = _auth.currentUser;
    if (firebaseUser != null) {
      print(
          'DEBUG: 🔑 Got Firebase Auth UID from Firebase Auth: ${firebaseUser.uid}');
      return firebaseUser.uid;
    }

    print(
        'DEBUG: ⚠️ Firebase Auth currentUser is null, trying to get from document...');

    // Nếu Firebase Auth null, lấy từ document user (field firebaseAuthUid)
    try {
      final userModel = await currentUserModel;
      if (userModel != null) {
        print('DEBUG: 🔍 Got userModel, email: ${userModel.email}');
        // Query lại document để lấy firebaseAuthUid
        final userQuery = await _firestore
            .collection('users')
            .where('email', isEqualTo: userModel.email)
            .limit(1)
            .get();

        if (userQuery.docs.isNotEmpty) {
          final docData = userQuery.docs.first.data();
          final firebaseAuthUid = docData['firebaseAuthUid']?.toString();
          print('DEBUG: 🔍 Document data - firebaseAuthUid: $firebaseAuthUid');
          if (firebaseAuthUid != null && firebaseAuthUid.isNotEmpty) {
            print(
                'DEBUG: 🔑 Got Firebase Auth UID from document: $firebaseAuthUid');
            return firebaseAuthUid;
          } else {
            print(
                'DEBUG: ⚠️ firebaseAuthUid field is empty or null in document');
          }
        } else {
          print('DEBUG: ⚠️ No document found with email: ${userModel.email}');
        }
      } else {
        print('DEBUG: ⚠️ currentUserModel returned null');
      }
    } catch (e) {
      print('DEBUG: ❌ Error getting Firebase Auth UID from document: $e');
    }

    return null;
  }

  // ========================================
  // ========================================
  // PRIVATE: _resolveEmailForUsername
  // MÔ TẢ: Map username -> email trước khi đăng nhập FirebaseAuth
  // ========================================
  Future<String?> _resolveEmailForUsername(String username) async {
    if (username.isEmpty) return null;

    // 1. Check if username is already an email format
    if (username.contains('@') && username.contains('.')) {
      print('DEBUG: Username is email format, using directly: $username');
      return username;
    }

    // 2. Map cục bộ cho các tài khoản cố định
    const localMappings = {
      'admin': 'admin@gmail.com',
    };
    if (localMappings.containsKey(username)) {
      return localMappings[username];
    }

    // 3. Thử đọc từ collection "username_index" (public read) nếu được cấu hình
    try {
      final doc = await _firestore
          .collection('username_index')
          .doc(username)
          .get(const GetOptions(source: Source.server));
      if (doc.exists) {
        final data = doc.data();
        final email = data?['email']?.toString();
        if (email != null && email.isNotEmpty) {
          return email;
        }
      }
    } catch (e) {
      print('DEBUG: Username index lookup failed: $e');
    }

    // 4. Try to find user by email in users collection (for students)
    try {
      print('DEBUG: Searching for user with email: $username');
      final querySnapshot = await _firestore
          .collection('users')
          .where('email', isEqualTo: username)
          .limit(1)
          .get();

      if (querySnapshot.docs.isNotEmpty) {
        final email = querySnapshot.docs.first.data()['email'] as String?;
        print('DEBUG: Found user with email: $email');
        return email;
      }
    } catch (e) {
      print('DEBUG: Email lookup in users collection failed: $e');
    }

    return null;
  }
}

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository.defaultClient();
});

final currentUserProvider = StreamProvider<UserModel?>((ref) {
  final authRepository = ref.watch(authRepositoryProvider);
  return authRepository.userModelStream;
});
