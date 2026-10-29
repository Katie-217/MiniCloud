// ========================================
// FILE: student_repository.dart (FIXED & UPDATED)
// MÔ TẢ: Repository sinh viên - Sử dụng UserModel & Client-side filtering
// ========================================

import 'dart:convert';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:http/http.dart' as http;
import '../../../domain/models/user_model.dart';
import '../../../core/config/users-role.dart';

class StudentRepository {
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  static const String _collection = 'users';

  // ========================================
  // HÀM: getAllStudents()
  // MÔ TẢ: Lấy tất cả User có role là Student
  // Chiến lược: Query toàn bộ -> Filter client để tránh Composite Index
  // ========================================
  static Future<List<UserModel>> getAllStudents() async {
    try {
      final querySnapshot = await _firestore.collection(_collection).get();

      final students = querySnapshot.docs
          .map((doc) {
            try {
              return UserModel.fromFirestore(doc);
            } catch (e) {
              return null;
            }
          })
          .where((u) => u != null && u.role == UserRole.student)
          .cast<UserModel>()
          .toList();

      students.sort((a, b) => a.name.compareTo(b.name));
      return students;
    } catch (e) {
      return [];
    }
  }

  // ========================================
  // HÀM: searchStudents()
  // MÔ TẢ: Tìm kiếm theo Tên hoặc Email (Tránh index)
  // ========================================
  static Future<List<UserModel>> searchStudents(String query) async {
    try {
      if (query.isEmpty) {
        return await getAllStudents();
      }

      final querySnapshot = await _firestore.collection(_collection).get();
      final queryLower = query.toLowerCase();

      final students = querySnapshot.docs
          .map((doc) {
            try {
              return UserModel.fromFirestore(doc);
            } catch (e) {
              return null;
            }
          })
          .where(
            (u) =>
                u != null &&
                u.role == UserRole.student &&
                (u.name.toLowerCase().contains(queryLower) ||
                    u.email.toLowerCase().contains(queryLower)),
          )
          .cast<UserModel>()
          .toList();

      students.sort((a, b) => a.name.compareTo(b.name));
      return students;
    } catch (e) {
      return [];
    }
  }

  // ========================================
  // HÀM: createStudent()
  // MÔ TẢ: Tạo sinh viên mới (Lưu UserModel)
  // ========================================
  static Future<String> createStudent(UserModel user) async {
    try {
      await _firestore
          .collection(_collection)
          .doc(user.uid)
          .set(user.toFirestore(), SetOptions(merge: true));
      return user.uid;
    } catch (e) {
      throw Exception('Lỗi tạo sinh viên: $e');
    }
  }

  // ========================================
  // HÀM: getStudentById()
  // MÔ TẢ: Lấy chi tiết sinh viên
  // ========================================
  static Future<UserModel?> getStudentById(String uid) async {
    try {
      final docSnapshot = await _firestore
          .collection(_collection)
          .doc(uid)
          .get();

      if (!docSnapshot.exists) return null;

      final user = UserModel.fromFirestore(docSnapshot);
      if (user.role != UserRole.student) return null;

      return user;
    } catch (e) {
      throw Exception('Lỗi lấy sinh viên: $e');
    }
  }

  // ========================================
  // HÀM: updateStudent()
  // MÔ TẢ: Cập nhật toàn bộ object
  // ========================================
  static Future<void> updateStudent(UserModel user) async {
    try {
      await _firestore
          .collection(_collection)
          .doc(user.uid)
          .update(user.toFirestore());
    } catch (e) {
      throw Exception('Lỗi cập nhật sinh viên: $e');
    }
  }

  // ========================================
  // HÀM: updateStudentProfile()
  // MÔ TẢ: Cập nhật từng trường (Name, Phone)
  // CASCADE UPDATE: Khi đổi name → cập nhật enrollments.studentName
  // ========================================
  static Future<void> updateStudentProfile(
    String uid, {
    String? name,
    String? phone,
  }) async {
    try {
      // Update users collection
      final updates = <String, dynamic>{};

      if (name != null) updates['name'] = name;
      if (phone != null) updates['phoneNumber'] = phone;
      if (updates.isNotEmpty) {
        updates['updatedAt'] = DateTime.now().toIso8601String();

        await _firestore.collection(_collection).doc(uid).update(updates);
      }

      // CASCADE UPDATE: If name changed, update enrollments collection
      if (name != null) {
        print('📝 Cascade update: Updating studentName in enrollments...');
        final enrollmentsSnapshot = await _firestore
            .collection('enrollments')
            .where('userId', isEqualTo: uid)
            .get();

        if (enrollmentsSnapshot.docs.isNotEmpty) {
          final batch = _firestore.batch();
          for (var doc in enrollmentsSnapshot.docs) {
            batch.update(doc.reference, {'studentName': name});
          }
          await batch.commit();
          print(
            '✅ Updated ${enrollmentsSnapshot.docs.length} enrollment records',
          );
        }
      }
    } catch (e) {
      throw Exception('Lỗi cập nhật: $e');
    }
  }

  // ========================================
  // HÀM: updateStudentEmail()
  // MÔ TẢ: Cập nhật email qua Cloud Function
  // Updates Authentication + Firestore
  // ========================================
  static Future<Map<String, dynamic>> updateStudentEmail(
    String uid,
    String newEmail,
  ) async {
    try {
      print('📧 Calling updateStudentEmailV2 function...');
      print('   UID: $uid');
      print('   New Email: $newEmail');

      // Call Gen2 HTTP Cloud Function (same as bulkCreateUsers pattern)
      final response = await http.post(
        Uri.parse(
          'http://localhost:5001/demo-minicloud/us-central1/updateStudentEmailV2',
        ),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'uid': uid, 'newEmail': newEmail}),
      );

      print('📞 Response status: ${response.statusCode}');
      print('📞 Response body: ${response.body}');

      if (response.statusCode == 200) {
        final result = json.decode(response.body);
        print('✅ Function returned: $result');
        return Map<String, dynamic>.from(result);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Failed to update email');
      }
    } catch (e) {
      print('❌ Error: $e');
      throw Exception('Lỗi cập nhật email: $e');
    }
  }

  // ========================================
  // HÀM: deleteStudent()
  // MÔ TẢ: CASCADE DELETE - Xóa hoàn toàn sinh viên khỏi hệ thống
  // Gọi Cloud Function để xóa: Authentication + Firestore + Enrollments
  // ========================================
  static Future<Map<String, dynamic>> deleteStudent(String uid) async {
    try {
      print('🗑️ Calling deleteStudentCompletely function...');
      print('   UID: $uid');

      // Call Cloud Function via HTTP
      final response = await http.post(
        Uri.parse(
          'http://localhost:5001/demo-minicloud/us-central1/deleteStudentCompletely',
        ),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'uid': uid}),
      );

      print('📡 Response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final result = json.decode(response.body) as Map<String, dynamic>;
        print('✅ Student deleted completely: ${result['deletionResults']}');
        return result;
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Failed to delete student');
      }
    } catch (e) {
      print('❌ Delete error: $e');
      throw Exception('Lỗi xóa sinh viên: $e');
    }
  }

  // ========================================
  // HÀM: getStudentStatistics()
  // MÔ TẢ: Thống kê đơn giản
  // ========================================
  static Future<Map<String, int>> getStudentStatistics() async {
    try {
      final allStudents = await getAllStudents();
      final activeStudents = allStudents.where((s) => s.isActive).toList();

      return {
        'total': allStudents.length,
        'active': activeStudents.length,
        'inactive': allStudents.length - activeStudents.length,
      };
    } catch (e) {
      return {'total': 0, 'active': 0, 'inactive': 0};
    }
  }

  // ========================================
  // HÀM: listenToStudents()
  // MÔ TẢ: Stream theo dõi danh sách sinh viên (client-side filter)
  // ========================================
  static Stream<List<UserModel>> listenToStudents() {
    return _firestore.collection(_collection).snapshots().map((snapshot) {
      final students = snapshot.docs
          .map((doc) {
            try {
              return UserModel.fromFirestore(doc);
            } catch (e) {
              return null;
            }
          })
          .where((u) => u != null && u.role == UserRole.student)
          .cast<UserModel>()
          .toList();

      students.sort((a, b) => a.name.compareTo(b.name));
      return students;
    });
  }

  // ==================================================================
  // NOTE: Các hàm liên quan đến Course/Group đã bị loại bỏ hoàn toàn
  // vì UserModel mới không còn chứa courseIds / groupIds.
  // Quản lý đăng ký khóa học / nhóm phải dùng collection riêng (enrollments, group_members...).
  // Các hàm dưới đây chỉ là placeholder để tránh lỗi compile tạm thời.
  // ==================================================================

  static Future<void> enrollStudentToCourse(String uid, String courseId) async {
    // TODO: Implement với collection enrollments
    // throw UnimplementedError('Chưa hỗ trợ với UserModel mới');
  }

  static Future<void> removeStudentFromCourse(
    String uid,
    String courseId,
  ) async {
    // TODO: Implement với collection enrollments
  }

  static Future<List<UserModel>> getStudentsByCourse(String courseId) async {
    // TODO: Query từ collection enrollments
    return [];
  }

  static Future<List<UserModel>> getStudentsByGroup(String groupId) async {
    // TODO: Query từ collection group_members hoặc tương tự
    return [];
  }

  static Future<void> addStudentToGroup(String uid, String groupId) async {
    // TODO: Implement
  }

  static Future<void> removeStudentFromGroup(String uid, String groupId) async {
    // TODO: Implement
  }

  static Future<List<UserModel>> getStudentsByIds(
    List<String> studentUids,
  ) async {
    // Tạm thời không dùng nữa hoặc implement lại nếu cần
    return [];
  }
}
