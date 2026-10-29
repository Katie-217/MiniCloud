// ========================================
// FILE: submission_repository.dart
// MÔ TẢ: Repository cho Submission - Root Collection
// REFACTORED: Di chuyển từ Sub-collection sang Root Collection
// ========================================

import 'package:cloud_firestore/cloud_firestore.dart';
import '../../../domain/models/submission_model.dart';

class SubmissionRepository {
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  // ✅ NEW: Root Collection instead of Sub-collection
  static const String _submissionCollectionName = 'submissions';

  // ========================================
  // HÀM: getSubmissionsForAssignment
  // MÔ TẢ: Lấy submissions từ Root Collection với where filter
  // ========================================
  static Future<List<SubmissionModel>> getSubmissionsForAssignment(String assignmentId) async {
    try {
      print('DEBUG: ========== FETCHING SUBMISSIONS ==========');
      print('DEBUG: 🔍 Fetching submissions for assignment: $assignmentId');
      print('DEBUG: 📂 Root Collection: $_submissionCollectionName');

      // ✅ NEW: Root Collection with where filter
      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('assignmentId', isEqualTo: assignmentId)
          .orderBy('submittedAt', descending: true)
          .get();

      print('DEBUG: 📋 Found ${snapshot.docs.length} submission documents');

      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
          print('DEBUG: ✅ Parsed submission: ${submission.id} by ${submission.studentName}');
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }

      print('DEBUG: ✅ Successfully loaded ${submissions.length} submissions');
      return submissions;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submissions: $e');
      return [];
    }
  }

  // ========================================
  // HÀM: getSubmissionsForStudent - NEW METHOD
  // MÔ TẢ: Lấy submissions của student (cho Dashboard)
  // ========================================
  static Future<List<SubmissionModel>> getSubmissionsForStudent(String studentId) async {
    try {
      print('DEBUG: 🔍 Fetching submissions for student: $studentId');

      // ✅ NEW: Root Collection with where filter
      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('studentId', isEqualTo: studentId)
          .orderBy('submittedAt', descending: true)
          .get();

      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }

      print('DEBUG: ✅ Found ${submissions.length} submissions for student');
      return submissions;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submissions for student: $e');
      return [];
    }
  }

  // ========================================
  // HÀM: createSubmission
  // MÔ TẢ: Tạo submission mới trong Root Collection
  // IMPORTANT: courseId, semesterId, groupId phải được set trước khi gọi
  // ========================================
  static Future<String> createSubmission(SubmissionModel submission) async {
    try {
      print('DEBUG: 📝 Creating submission for assignment: ${submission.assignmentId}');
      print('DEBUG: 📝 Student: ${submission.studentName}');
      print('DEBUG: 📝 CourseId: ${submission.courseId}');
      print('DEBUG: 📝 SemesterId: ${submission.semesterId}');
      print('DEBUG: 📝 GroupId: ${submission.groupId}');

      // ✅ VALIDATION: Đảm bảo required fields đã được set
      if (submission.courseId.isEmpty) {
        throw Exception('CourseId is required for Root Collection');
      }
      if (submission.semesterId.isEmpty) {
        throw Exception('SemesterId is required for Root Collection');
      }
      if (submission.groupId.isEmpty) {
        throw Exception('GroupId is required for Root Collection');
      }

      // ✅ NEW: Add to Root Collection
      final docRef = await _firestore
          .collection(_submissionCollectionName)
          .add(submission.toMap());

      print('DEBUG: ✅ Created submission with ID: ${docRef.id}');
      return docRef.id;
    } catch (e) {
      print('DEBUG: ❌ Error creating submission: $e');
      throw Exception('Failed to create submission: $e');
    }
  }

  // ========================================
  // HÀM: updateSubmission
  // MÔ TẢ: Cập nhật submission trong Root Collection
  // ========================================
  static Future<void> updateSubmission(SubmissionModel submission) async {
    try {
      print('DEBUG: 📝 Updating submission: ${submission.id}');

      await _firestore
          .collection(_submissionCollectionName)
          .doc(submission.id)
          .update(submission.toMap());

      print('DEBUG: ✅ Updated submission: ${submission.id}');
    } catch (e) {
      print('DEBUG: ❌ Error updating submission: $e');
      throw Exception('Failed to update submission: $e');
    }
  }

  // ========================================
  // HÀM: deleteSubmission
  // MÔ TẢ: Xóa submission từ Root Collection
  // ========================================
  static Future<void> deleteSubmission(String submissionId) async {
    try {
      print('DEBUG: 🗑️ Deleting submission: $submissionId');

      await _firestore
          .collection(_submissionCollectionName)
          .doc(submissionId)
          .delete();

      print('DEBUG: ✅ Deleted submission: $submissionId');
    } catch (e) {
      print('DEBUG: ❌ Error deleting submission: $e');
      throw Exception('Failed to delete submission: $e');
    }
  }

  // ========================================
  // HÀM: getSubmissionById
  // MÔ TẢ: Lấy submission cụ thể theo ID từ Root Collection
  // ========================================
  static Future<SubmissionModel?> getSubmissionById(String submissionId) async {
    try {
      print('DEBUG: 🔍 Fetching submission by ID: $submissionId');

      final doc = await _firestore
          .collection(_submissionCollectionName)
          .doc(submissionId)
          .get();

      if (!doc.exists) {
        print('DEBUG: ⚠️ Submission not found: $submissionId');
        return null;
      }

      final submission = SubmissionModel.fromMap({
        'id': doc.id,
        ...doc.data() as Map<String, dynamic>,
      });

      print('DEBUG: ✅ Found submission: ${submission.id}');
      return submission;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submission by ID: $e');
      return null;
    }
  }

  // ========================================
  // HÀM: getSubmissionsByCourse - NEW METHOD
  // MÔ TẢ: Lấy submissions theo course (cho Instructor)
  // ========================================
  static Future<List<SubmissionModel>> getSubmissionsByCourse(String courseId) async {
    try {
      print('DEBUG: 🔍 Fetching submissions for course: $courseId');

      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('courseId', isEqualTo: courseId)
          .orderBy('submittedAt', descending: true)
          .get();

      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }

      print('DEBUG: ✅ Found ${submissions.length} submissions for course');
      return submissions;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submissions by course: $e');
      return [];
    }
  }

  // ========================================
  // HÀM: getSubmissionsByGroup - NEW METHOD
  // MÔ TẢ: Lấy submissions theo group (cho filtering)
  // ========================================
  static Future<List<SubmissionModel>> getSubmissionsByGroup(String groupId) async {
    try {
      print('DEBUG: 🔍 Fetching submissions for group: $groupId');

      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('groupId', isEqualTo: groupId)
          .orderBy('submittedAt', descending: true)
          .get();

      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }

      print('DEBUG: ✅ Found ${submissions.length} submissions for group');
      return submissions;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submissions by group: $e');
      return [];
    }
  }

  // ========================================
  // HÀM: getSubmissionsBySemester - NEW METHOD
  // MÔ TẢ: Lấy submissions theo semester (cho CSV export)
  // ========================================
  static Future<List<SubmissionModel>> getSubmissionsBySemester(String semesterId) async {
    try {
      print('DEBUG: 🔍 Fetching submissions for semester: $semesterId');

      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('semesterId', isEqualTo: semesterId)
          .orderBy('submittedAt', descending: true)
          .get();

      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }

      print('DEBUG: ✅ Found ${submissions.length} submissions for semester');
      return submissions;
    } catch (e) {
      print('DEBUG: ❌ Error fetching submissions by semester: $e');
      return [];
    }
  }

  // ========================================
  // HÀM: getStudentSubmissionForAssignment
  // MÔ TẢ: Lấy submission của student cụ thể cho assignment cụ thể
  // ========================================
  static Future<SubmissionModel?> getStudentSubmissionForAssignment(
    String assignmentId,
    String studentId,
  ) async {
    try {
      print('DEBUG: 🔍 Fetching submission for assignment: $assignmentId, student: $studentId');

      final snapshot = await _firestore
          .collection(_submissionCollectionName)
          .where('assignmentId', isEqualTo: assignmentId)
          .where('studentId', isEqualTo: studentId)
          .limit(1)
          .get();

      if (snapshot.docs.isEmpty) {
        print('DEBUG: ⚠️ No submission found');
        return null;
      }

      final doc = snapshot.docs.first;
      final submission = SubmissionModel.fromMap({
        'id': doc.id,
        ...doc.data() as Map<String, dynamic>,
      });

      print('DEBUG: ✅ Found submission: ${submission.id}');
      return submission;
    } catch (e) {
      print('DEBUG: ❌ Error fetching student submission: $e');
      return null;
    }
  }

  // ========================================
  // HÀM: listenToSubmissions - REAL-TIME
  // MÔ TẢ: Stream để theo dõi submissions real-time
  // ========================================
  static Stream<List<SubmissionModel>> listenToSubmissions({
    String? assignmentId,
    String? studentId,
    String? courseId,
  }) {
    Query query = _firestore.collection(_submissionCollectionName);

    if (assignmentId != null) {
      query = query.where('assignmentId', isEqualTo: assignmentId);
    }

    if (studentId != null) {
      query = query.where('studentId', isEqualTo: studentId);
    }

    if (courseId != null) {
      query = query.where('courseId', isEqualTo: courseId);
    }

    return query
        .orderBy('submittedAt', descending: true)
        .snapshots()
        .map((snapshot) {
      final submissions = <SubmissionModel>[];
      for (var doc in snapshot.docs) {
        try {
          final submission = SubmissionModel.fromMap({
            'id': doc.id,
            ...doc.data() as Map<String, dynamic>,
          });
          submissions.add(submission);
        } catch (e) {
          print('DEBUG: ⚠️ Error parsing submission doc ${doc.id}: $e');
        }
      }
      return submissions;
    });
  }

  // ========================================
  // HÀM: bulkDeleteSubmissions - CLEANUP
  // MÔ TẢ: Xóa hàng loạt submissions (khi xóa assignment/course)
  // ========================================
  static Future<void> bulkDeleteSubmissions({
    String? assignmentId,
    String? courseId,
    String? semesterId,
  }) async {
    try {
      Query query = _firestore.collection(_submissionCollectionName);

      if (assignmentId != null) {
        query = query.where('assignmentId', isEqualTo: assignmentId);
      }

      if (courseId != null) {
        query = query.where('courseId', isEqualTo: courseId);
      }

      if (semesterId != null) {
        query = query.where('semesterId', isEqualTo: semesterId);
      }

      final snapshot = await query.get();
      final batch = _firestore.batch();

      for (var doc in snapshot.docs) {
        batch.delete(doc.reference);
      }

      await batch.commit();
      print('DEBUG: ✅ Bulk deleted ${snapshot.docs.length} submissions');
    } catch (e) {
      print('DEBUG: ❌ Error bulk deleting submissions: $e');
      throw Exception('Failed to bulk delete submissions: $e');
    }
  }

  // ========================================
  // HÀM: getSubmissionStats - ANALYTICS
  // MÔ TẢ: Lấy thống kê submissions (cho Dashboard)
  // ========================================
  static Future<Map<String, dynamic>> getSubmissionStats({
    String? assignmentId,
    String? courseId,
    String? semesterId,
  }) async {
    try {
      Query query = _firestore.collection(_submissionCollectionName);

      if (assignmentId != null) {
        query = query.where('assignmentId', isEqualTo: assignmentId);
      }

      if (courseId != null) {
        query = query.where('courseId', isEqualTo: courseId);
      }

      if (semesterId != null) {
        query = query.where('semesterId', isEqualTo: semesterId);
      }

      final snapshot = await query.get();

      int totalSubmissions = snapshot.docs.length;
      int gradedSubmissions = 0;
      int lateSubmissions = 0;
      double totalScore = 0;
      int scoredSubmissions = 0;

      for (var doc in snapshot.docs) {
        final data = doc.data() as Map<String, dynamic>;

        if (data['gradedAt'] != null) {
          gradedSubmissions++;
        }

        if (data['isLate'] == true) {
          lateSubmissions++;
        }

        if (data['score'] != null) {
          totalScore += (data['score'] as num).toDouble();
          scoredSubmissions++;
        }
      }

      return {
        'totalSubmissions': totalSubmissions,
        'gradedSubmissions': gradedSubmissions,
        'lateSubmissions': lateSubmissions,
        'averageScore': scoredSubmissions > 0 ? totalScore / scoredSubmissions : 0.0,
        'gradingProgress': totalSubmissions > 0 ? (gradedSubmissions / totalSubmissions * 100).round() : 0,
      };
    } catch (e) {
      print('DEBUG: ❌ Error getting submission stats: $e');
      return {};
    }
  }
}
