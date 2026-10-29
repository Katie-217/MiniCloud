// ========================================
// FILE: material_tracking_controller.dart
// MÔ TẢ: Controller quản lý business logic cho Material Tracking
// Clean Architecture: Application Layer
// ========================================

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../data/repositories/material/material_tracking_repository.dart';
import '../../../../data/repositories/course/enrollment_repository.dart';
import '../../../../domain/models/material_tracking_model.dart';

// ========================================
// PROVIDER: materialTrackingRepositoryProvider
// ========================================
final materialTrackingRepositoryProvider = Provider<MaterialTrackingRepository>((ref) {
  return MaterialTrackingRepository();
});

// ========================================
// PROVIDER: materialTrackingControllerProvider
// ========================================
final materialTrackingControllerProvider = Provider<MaterialTrackingController>((ref) {
  return MaterialTrackingController(
    trackingRepository: ref.read(materialTrackingRepositoryProvider),
    enrollmentRepository: EnrollmentRepository(),
  );
});

// ========================================
// CLASS: MaterialTrackingController
// MÔ TẢ: Business logic authority cho Material Tracking
// ========================================
class MaterialTrackingController {
  final MaterialTrackingRepository _trackingRepository;
  final EnrollmentRepository _enrollmentRepository;

  MaterialTrackingController({
    required MaterialTrackingRepository trackingRepository,
    required EnrollmentRepository enrollmentRepository,
  }) : _trackingRepository = trackingRepository,
       _enrollmentRepository = enrollmentRepository;

  // ========================================
  // HÀM: handleViewEvent()
  // MÔ TẢ: Xử lý sự kiện sinh viên "xem" tài liệu
  // LOGIC: Lấy groupId từ Enrollment, sau đó ghi nhật ký
  // ========================================
  Future<void> handleViewEvent({
    required String materialId,
    required String courseId,
    required String studentId,
  }) async {
    try {
      print('DEBUG: 👀 Handling view event - materialId: $materialId, studentId: $studentId');

      // 1. Lấy groupId từ Enrollment (QUAN TRỌNG cho thống kê theo nhóm)
      final enrollment = await _enrollmentRepository.getEnrollment(courseId, studentId);

      if (enrollment == null) {
        throw Exception('Sinh viên chưa được ghi danh vào khóa học này');
      }

      final groupId = enrollment.groupId;
      if (groupId.isEmpty) {
        throw Exception('Sinh viên chưa được phân nhóm'); // Theo Strict Enrollment, không bao giờ xảy ra
      }

      // 2. Tạo tracking record
      final trackingId = MaterialTrackingModel.generateId(
        materialId: materialId,
        studentId: studentId,
      );

      final trackingData = MaterialTrackingModel(
        id: trackingId,
        materialId: materialId,
        courseId: courseId,
        studentId: studentId,
        groupId: groupId, // ✅ Lưu groupId để Giảng viên xem thống kê
        hasViewed: true,
        hasDownloaded: false,
        lastViewedAt: DateTime.now(),
      );

      // 3. Ghi nhật ký vào Firebase
      await _trackingRepository.logViewEvent(trackingData);

      print('✅ Successfully logged view event for student $studentId, group $groupId');
    } catch (e) {
      print('❌ Error handling view event: $e');
      rethrow;
    }
  }

  // ========================================
  // HÀM: handleDownloadEvent()
  // MÔ TẢ: Xử lý sự kiện sinh viên "tải" tài liệu
  // LOGIC: Tương tự handleViewEvent, nhưng gọi logDownloadEvent
  // ========================================
  Future<void> handleDownloadEvent({
    required String materialId,
    required String courseId,
    required String studentId,
  }) async {
    try {
      print('DEBUG: 📥 Handling download event - materialId: $materialId, studentId: $studentId');

      // 1. Lấy groupId từ Enrollment
      final enrollment = await _enrollmentRepository.getEnrollment(courseId, studentId);

      if (enrollment == null) {
        throw Exception('Sinh viên chưa được ghi danh vào khóa học này');
      }

      final groupId = enrollment.groupId;
      if (groupId.isEmpty) {
        throw Exception('Sinh viên chưa được phân nhóm'); // Theo Strict Enrollment, không bao giờ xảy ra
      }

      // 2. Tạo tracking record
      final trackingId = MaterialTrackingModel.generateId(
        materialId: materialId,
        studentId: studentId,
      );

      final trackingData = MaterialTrackingModel(
        id: trackingId,
        materialId: materialId,
        courseId: courseId,
        studentId: studentId,
        groupId: groupId, // ✅ Lưu groupId để Giảng viên xem thống kê
        hasViewed: true, // Auto-mark as viewed when downloading
        hasDownloaded: true,
        lastViewedAt: DateTime.now(),
        lastDownloadedAt: DateTime.now(),
      );

      // 3. Ghi nhật ký vào Firebase
      await _trackingRepository.logDownloadEvent(trackingData);

      print('✅ Successfully logged download event for student $studentId, group $groupId');
    } catch (e) {
      print('❌ Error handling download event: $e');
      rethrow;
    }
  }

  // ========================================
  // HÀM: getStatsForMaterial()
  // MÔ TẢ: Lấy thống kê cho một tài liệu cụ thể
  // RETURN: MaterialStats với breakdown theo nhóm
  // ========================================
  Future<MaterialStats> getStatsForMaterial(String materialId) async {
    try {
      print('DEBUG: 📊 Getting stats for materialId: $materialId');

      final trackingList = await _trackingRepository.getStatsForMaterial(materialId);
      final stats = MaterialStats.fromTrackingList(materialId, trackingList);

      print('DEBUG: ✅ Material stats - totalViews: ${stats.totalViews}, totalDownloads: ${stats.totalDownloads}');
      print('DEBUG: 📊 Views by group: ${stats.viewsByGroup}');
      print('DEBUG: 📊 Downloads by group: ${stats.downloadsByGroup}');

      return stats;
    } catch (e) {
      print('❌ Error getting material stats: $e');
      rethrow;
    }
  }

  // ========================================
  // HÀM: getStatsForCourse()
  // MÔ TẢ: Lấy thống kê cho tất cả tài liệu trong khóa học
  // ========================================
  Future<List<MaterialTrackingModel>> getStatsForCourse(String courseId) async {
    try {
      return await _trackingRepository.getStatsForCourse(courseId);
    } catch (e) {
      throw Exception('Failed to get course stats: $e');
    }
  }

  // ========================================
  // HÀM: getStudentActivity()
  // MÔ TẢ: Lấy lịch sử hoạt động của sinh viên
  // ========================================
  Future<List<MaterialTrackingModel>> getStudentActivity(
    String studentId, {
    String? courseId,
  }) async {
    try {
      return await _trackingRepository.getStudentActivity(
        studentId,
        courseId: courseId,
      );
    } catch (e) {
      throw Exception('Failed to get student activity: $e');
    }
  }

  // ========================================
  // HÀM: getGroupStats()
  // MÔ TẢ: Lấy thống kê theo nhóm cho Giảng viên
  // RETURN: Map<groupId, List<MaterialTrackingModel>>
  // ========================================
  Future<Map<String, List<MaterialTrackingModel>>> getGroupStats(
    String materialId,
  ) async {
    try {
      return await _trackingRepository.getGroupStats(materialId);
    } catch (e) {
      throw Exception('Failed to get group stats: $e');
    }
  }

  // ========================================
  // HÀM: hasStudentViewedMaterial()
  // MÔ TẢ: Kiểm tra sinh viên đã xem tài liệu chưa
  // ========================================
  Future<bool> hasStudentViewedMaterial(
    String materialId,
    String studentId,
  ) async {
    try {
      final trackingRecord = await _trackingRepository.getTrackingRecord(
        materialId,
        studentId,
      );

      return trackingRecord?.hasViewed ?? false;
    } catch (e) {
      print('❌ Error checking if student viewed material: $e');
      return false;
    }
  }

  // ========================================
  // HÀM: hasStudentDownloadedMaterial()
  // MÔ TẢ: Kiểm tra sinh viên đã tải tài liệu chưa
  // ========================================
  Future<bool> hasStudentDownloadedMaterial(
    String materialId,
    String studentId,
  ) async {
    try {
      final trackingRecord = await _trackingRepository.getTrackingRecord(
        materialId,
        studentId,
      );

      return trackingRecord?.hasDownloaded ?? false;
    } catch (e) {
      print('❌ Error checking if student downloaded material: $e');
      return false;
    }
  }

  // ========================================
  // HÀM: getDetailedStatsForInstructor()
  // MÔ TẢ: Lấy thống kê chi tiết cho Giảng viên UI
  // RETURN: Structured data cho dashboard
  // ========================================
  Future<Map<String, dynamic>> getDetailedStatsForInstructor(
    String materialId,
  ) async {
    try {
      final stats = await getStatsForMaterial(materialId);
      final groupStats = await getGroupStats(materialId);

      // Build detailed breakdown
      final Map<String, dynamic> detailedStats = {
        'overview': {
          'totalViews': stats.totalViews,
          'totalDownloads': stats.totalDownloads,
          'totalStudentsInteracted': stats.recentActivity.length,
        },
        'byGroup': {},
        'recentActivity': stats.recentActivity.take(5).map((tracking) => {
          'studentId': tracking.studentId,
          'groupId': tracking.groupId,
          'hasViewed': tracking.hasViewed,
          'hasDownloaded': tracking.hasDownloaded,
          'lastViewedAt': tracking.lastViewedAt.toIso8601String(),
          'lastDownloadedAt': tracking.lastDownloadedAt?.toIso8601String(),
        }).toList(),
      };

      // Process group stats
      for (final entry in groupStats.entries) {
        final groupId = entry.key;
        final trackingList = entry.value;

        final groupViews = trackingList.where((t) => t.hasViewed).length;
        final groupDownloads = trackingList.where((t) => t.hasDownloaded).length;

        detailedStats['byGroup'][groupId] = {
          'totalStudents': trackingList.length,
          'views': groupViews,
          'downloads': groupDownloads,
          'viewRate': trackingList.isNotEmpty ? (groupViews / trackingList.length * 100).round() : 0,
          'downloadRate': trackingList.isNotEmpty ? (groupDownloads / trackingList.length * 100).round() : 0,
        };
      }

      return detailedStats;
    } catch (e) {
      throw Exception('Failed to get detailed stats: $e');
    }
  }

  // ========================================
  // HÀM: cleanupTrackingForMaterial()
  // MÔ TẢ: Xóa tất cả tracking records khi xóa tài liệu
  // ========================================
  Future<void> cleanupTrackingForMaterial(String materialId) async {
    try {
      await _trackingRepository.bulkDeleteTrackingForMaterial(materialId);
      print('✅ Successfully cleaned up tracking records for material $materialId');
    } catch (e) {
      throw Exception('Failed to cleanup tracking records: $e');
    }
  }

  // ========================================
  // HÀM: listenToMaterialStats()
  // MÔ TẢ: Stream để theo dõi thống kê real-time
  // ========================================
  Stream<MaterialStats> listenToMaterialStats(String materialId) {
    return _trackingRepository.listenToMaterialStats(materialId).map(
      (trackingList) => MaterialStats.fromTrackingList(materialId, trackingList),
    );
  }
}
