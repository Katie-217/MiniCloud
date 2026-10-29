// ========================================
// FILE: user_session_service.dart
// MÔ TẢ: Service cho SharedPreferences - Clean Architecture Compliant
// QUAN TRỌNG: Chỉ làm việc với SharedPreferences, KHÔNG import Firebase!
// ========================================

import 'package:shared_preferences/shared_preferences.dart';
import '../../../domain/models/user_model.dart';

// ========================================
// CLASS: UserSessionService
// MÔ TẢ: Quản lý session với SharedPreferences - Clean Architecture
// ========================================
class UserSessionService {
  static const String _isLoggedInKey = 'is_logged_in';
  static const String _userEmailKey = 'user_email';
  static const String _userDisplayNameKey = 'user_display_name';
  static const String _userUidKey = 'user_uid';
  static const String _userRoleKey = 'user_role';
  static const String _userNameKey = 'user_name';
  static const String _firebaseIdTokenKey = 'firebase_id_token';
  static const String _firebaseRefreshTokenKey = 'firebase_refresh_token';

  // ========================================
  // HÀM: saveUserSession - Nhận UserModel
  // MÔ TẢ: Lưu session từ UserModel vào SharedPreferences
  // ========================================
  static Future<void> saveUserSession(UserModel user) async {
    try {
      print('DEBUG: 💾 Saving user session to SharedPreferences: ${user.email}');
      final prefs = await SharedPreferences.getInstance();

      final success = await prefs.setBool(_isLoggedInKey, true);
      await prefs.setString(_userEmailKey, user.email);
      await prefs.setString(_userDisplayNameKey, user.displayName);
      await prefs.setString(_userUidKey, user.uid);
      await prefs.setString(_userRoleKey, user.role.name);
      await prefs.setString(_userNameKey, user.name);

      // Verify session was saved
      final isLoggedIn = prefs.getBool(_isLoggedInKey) ?? false;
      final savedUid = prefs.getString(_userUidKey);
      print('DEBUG: ✅ Session saved - isLoggedIn: $isLoggedIn, uid: $savedUid');
    } catch (e) {
      print('DEBUG: ❌ Error saving session: $e');
    }
  }

  // ========================================
  // HÀM: isUserLoggedIn
  // MÔ TẢ: Kiểm tra có user đã đăng nhập không
  // ========================================
  static Future<bool> isUserLoggedIn() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      return prefs.getBool(_isLoggedInKey) ?? false;
    } catch (e) {
      return false;
    }
  }

  // ========================================
  // HÀM: getUserSessionData - Trả về Map cho compatibility
  // MÔ TẢ: Lấy thông tin session từ SharedPreferences
  // ========================================
  static Future<Map<String, String>?> getUserSessionData() async {
    try {
      final prefs = await SharedPreferences.getInstance();

      final isLoggedIn = prefs.getBool(_isLoggedInKey) ?? false;
      if (!isLoggedIn) return null;

      return {
        'uid': prefs.getString(_userUidKey) ?? '',
        'email': prefs.getString(_userEmailKey) ?? '',
        'displayName': prefs.getString(_userDisplayNameKey) ?? '',
        'name': prefs.getString(_userNameKey) ?? '',
        'role': prefs.getString(_userRoleKey) ?? 'student',
      };
    } catch (e) {
      return null;
    }
  }

  // ========================================
  // HÀM: clearUserSession
  // MÔ TẢ: Xóa tất cả session data khỏi SharedPreferences
  // ========================================
  static Future<void> clearUserSession() async {
    try {
      print('DEBUG: 🗑️ Clearing user session from SharedPreferences');
      final prefs = await SharedPreferences.getInstance();

      await prefs.setBool(_isLoggedInKey, false);
      await prefs.remove(_userEmailKey);
      await prefs.remove(_userDisplayNameKey);
      await prefs.remove(_userUidKey);
      await prefs.remove(_userRoleKey);
      await prefs.remove(_userNameKey);
      await prefs.remove(_firebaseIdTokenKey);
      await prefs.remove(_firebaseRefreshTokenKey);

      // KHÔNG clear tất cả SharedPreferences vì có thể có dữ liệu khác
      // await prefs.clear(); // Đã xóa để tránh xóa dữ liệu khác
      print('DEBUG: ✅ Session cleared');
    } catch (e) {
      print('DEBUG: ❌ Error clearing session: $e');
    }
  }

  // ========================================
  // HÀM: hasValidSession
  // MÔ TẢ: Kiểm tra có session hợp lệ không (chỉ SharedPreferences)
  // ========================================
  static Future<bool> hasValidSession() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final isLoggedIn = prefs.getBool(_isLoggedInKey) ?? false;
      final uid = prefs.getString(_userUidKey) ?? '';
      final email = prefs.getString(_userEmailKey) ?? '';

      final hasSession = isLoggedIn && uid.isNotEmpty;
      print('DEBUG: 🔍 Checking SharedPreferences session - isLoggedIn: $isLoggedIn, uid: $uid, email: $email, hasSession: $hasSession');

      return hasSession;
    } catch (e) {
      print('DEBUG: ❌ Error checking session: $e');
      return false;
    }
  }

  // ========================================
  // HÀM: getStoredUserId
  // MÔ TẢ: Lấy nhanh user ID từ SharedPreferences
  // ========================================
  static Future<String?> getStoredUserId() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      return prefs.getString(_userUidKey);
    } catch (e) {
      return null;
    }
  }
}
