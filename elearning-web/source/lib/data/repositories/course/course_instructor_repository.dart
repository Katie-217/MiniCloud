// ========================================
// FILE: course_instructor_repository.dart
// MÔ TẢ: Repository cho Course - Data Layer dành cho GIẢNG VIÊN
// ========================================

import 'package:cloud_firestore/cloud_firestore.dart';
import '../../../domain/models/course_model.dart';
import 'enrollment_repository.dart';

// ========================================
// CLASS: CourseInstructorRepository - Data Access cho Giảng viên
// MÔ TẢ: Xử lý truy vấn Firestore cho courses mà giảng viên phụ trách
// ========================================
class CourseInstructorRepository {
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  static const String _collection = 'course_of_study';

  // ========================================
  // HÀM: getInstructorCourses - Lấy courses mà giảng viên phụ trách
  // MÔ TẢ: Query courses theo instructor field (string UID)
  // ========================================
  static Future<List<CourseModel>> getInstructorCourses(
      String instructorUid) async {
    try {
      print('DEBUG: 🔍 Querying courses for instructor: $instructorUid');
      print('DEBUG: 🔍 Collection: $_collection');
      print('DEBUG: 🔍 Query: where("instructor", isEqualTo: "$instructorUid")');

      // Query courses where instructor field matches instructorUid
      final querySnapshot = await _firestore
          .collection(_collection)
          .where('instructor', isEqualTo: instructorUid)
          .get();

      print(
          'DEBUG: 📚 Found ${querySnapshot.docs.length} courses for instructor');

      // Debug: In ra tất cả courses để kiểm tra
      if (querySnapshot.docs.isEmpty) {
        print('DEBUG: ⚠️ No courses found! Checking all courses in collection...');
        final allCourses = await _firestore.collection(_collection).limit(5).get();
        print('DEBUG: 📋 Sample courses in collection:');
        for (var doc in allCourses.docs) {
          final data = doc.data();
          print('DEBUG:   - Doc ID: ${doc.id}');
          print('DEBUG:     instructor field: ${data['instructor']}');
          print('DEBUG:     name: ${data['name']}');
        }
      } else {
        print('DEBUG: ✅ Courses found:');
        for (var doc in querySnapshot.docs) {
          print('DEBUG:   - ${doc.data()['name']} (${doc.data()['code']})');
        }
      }

      final courses = querySnapshot.docs.map((doc) {
        return CourseModel.fromFirestore(doc);
      }).toList();

      // Sort by semester and course name for better UX
      courses.sort((a, b) {
        final semesterCompare = b.semester.compareTo(a.semester);
        if (semesterCompare != 0) return semesterCompare;
        return a.name.compareTo(b.name);
      });

      return courses;
    } catch (e) {
      print(
          'DEBUG: ❌ CourseInstructorRepository.getInstructorCourses error: $e');
      throw Exception('Failed to get instructor courses: $e');
    }
  }

  // ========================================
  // HÀM: getInstructorCoursesBySemester - Lấy courses theo semester
  // MÔ TẢ: Query courses của giảng viên theo semester cụ thể
  // ========================================
  static Future<List<CourseModel>> getInstructorCoursesBySemester(
      String instructorUid, String semester) async {
    try {
      print(
          'DEBUG: 🔍 Querying courses for instructor: $instructorUid, semester: $semester');

      final querySnapshot = await _firestore
          .collection(_collection)
          .where('instructor', isEqualTo: instructorUid)
          .where('semester', isEqualTo: semester)
          .get();

      print(
          'DEBUG: 📚 Found ${querySnapshot.docs.length} courses for instructor in semester $semester');

      return querySnapshot.docs.map((doc) {
        return CourseModel.fromFirestore(doc);
      }).toList();
    } catch (e) {
      print(
          'DEBUG: ❌ CourseInstructorRepository.getInstructorCoursesBySemester error: $e');
      throw Exception('Failed to get instructor courses by semester: $e');
    }
  }

  // ========================================
  // HÀM: getCourseById - Lấy course cụ thể (cho giảng viên)
  // MÔ TẢ: Lấy course theo ID với validation instructor
  // ========================================
  static Future<CourseModel?> getCourseById(String courseId,
      {String? instructorUid}) async {
    try {
      print('DEBUG: 🔍 Getting course by ID: $courseId');

      final docSnapshot =
          await _firestore.collection(_collection).doc(courseId).get();

      if (!docSnapshot.exists) {
        print('DEBUG: ❌ Course not found: $courseId');
        return null;
      }

      final data = docSnapshot.data()!;

      // Optional: Validate instructor ownership
      if (instructorUid != null && data['instructor'] != instructorUid) {
        print(
            'DEBUG: ❌ Course $courseId not owned by instructor $instructorUid');
        throw Exception('Access denied: Course not owned by instructor');
      }

      return CourseModel.fromFirestore(docSnapshot);
    } catch (e) {
      print('DEBUG: ❌ CourseInstructorRepository.getCourseById error: $e');
      rethrow;
    }
  }

  // ========================================
  // HÀM: createCourse - Tạo course mới (cho giảng viên)
  // MÔ TẢ: Tạo course mới với instructor field
  // ========================================
  static Future<bool> createCourse(
      CourseModel course, String instructorUid) async {
    try {
      print('DEBUG: 📝 Creating course for instructor: $instructorUid');

      // Ensure instructor field is set and status is always 'active'
      final courseData = course.toFirestore();
      courseData['instructor'] = instructorUid;
      courseData['status'] =
          'active'; // Always set status to 'active' for new courses
      courseData['createdAt'] = FieldValue.serverTimestamp();
      courseData['updatedAt'] = FieldValue.serverTimestamp();

      await _firestore.collection(_collection).add(courseData);

      print('DEBUG: ✅ Course created successfully');
      return true;
    } catch (e) {
      print('DEBUG: ❌ CourseInstructorRepository.createCourse error: $e');
      return false;
    }
  }

  // ========================================
  // HÀM: updateCourse - Cập nhật course (cho giảng viên)
  // MÔ TẢ: Cập nhật course với validation instructor ownership
  // ========================================
  static Future<bool> updateCourse(
      String courseId, CourseModel course, String instructorUid) async {
    try {
      print(
          'DEBUG: 📝 Updating course: $courseId for instructor: $instructorUid');

      // First validate instructor ownership
      final existingCourse =
          await getCourseById(courseId, instructorUid: instructorUid);
      if (existingCourse == null) {
        throw Exception('Course not found or access denied');
      }

      final courseData = course.toFirestore();
      courseData['instructor'] =
          instructorUid; // Ensure instructor field remains
      courseData['updatedAt'] = FieldValue.serverTimestamp();

      await _firestore.collection(_collection).doc(courseId).update(courseData);

      print('DEBUG: ✅ Course updated successfully');
      return true;
    } catch (e) {
      print('DEBUG: ❌ CourseInstructorRepository.updateCourse error: $e');
      return false;
    }
  }

  // ========================================
  // DEPRECATED METHODS - Use EnrollmentRepository instead
  // ========================================

  @Deprecated('Use EnrollmentRepository.enrollStudent() instead')
  static Future<bool> addStudentToCourse(
      String courseId, String studentUid, String instructorUid) async {
    throw UnimplementedError(
        'This method is deprecated. Use EnrollmentRepository.enrollStudent() instead.');
  }

  @Deprecated('Use EnrollmentRepository.unenrollStudent() instead')
  static Future<bool> removeStudentFromCourse(
      String courseId, String studentUid, String instructorUid) async {
    throw UnimplementedError(
        'This method is deprecated. Use EnrollmentRepository.unenrollStudent() instead.');
  }

  // ========================================
  // HÀM: getStudentEnrollmentStats - Thống kê enrollment cho giảng viên
  // MÔ TẢ: Lấy thống kê số lượng students trong các courses
  // SửDỤNG: EnrollmentRepository để đếm students thực tế
  // ========================================
  static Future<Map<String, int>> getStudentEnrollmentStats(
      String instructorUid) async {
    try {
      final enrollmentRepo = EnrollmentRepository();
      final courses = await getInstructorCourses(instructorUid);

      int totalStudents = 0;
      int activeCourses = 0;

      for (final course in courses) {
        if (course.status == 'active') {
          activeCourses++;
          // 🔄 SửDỤNG EnrollmentRepository thay vì course.students
          final studentCount =
              await enrollmentRepo.countStudentsInCourse(course.id);
          totalStudents += studentCount;
        }
      }

      return {
        'totalCourses': courses.length,
        'activeCourses': activeCourses,
        'totalStudents': totalStudents,
      };
    } catch (e) {
      print(
          'DEBUG: ❌ CourseInstructorRepository.getStudentEnrollmentStats error: $e');
      return {
        'totalCourses': 0,
        'activeCourses': 0,
        'totalStudents': 0,
      };
    }
  }
}
