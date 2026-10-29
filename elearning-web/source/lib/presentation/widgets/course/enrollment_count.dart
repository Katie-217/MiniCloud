import 'package:flutter/material.dart';
import 'package:elearning_management_app/data/repositories/course/enrollment_repository.dart';

/// Display the real active enrollment count instead of a permanent placeholder.
class EnrollmentCount extends StatefulWidget {
  final String courseId;
  const EnrollmentCount({super.key, required this.courseId});
  @override
  State<EnrollmentCount> createState() => _EnrollmentCountState();
}

class _EnrollmentCountState extends State<EnrollmentCount> {
  late Future<int> _count;
  void _load() {
    _count = EnrollmentRepository().countStudentsInCourse(widget.courseId);
  }
  @override
  void initState() { super.initState(); _load(); }
  @override
  void didUpdateWidget(EnrollmentCount oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.courseId != widget.courseId) _load();
  }
  @override
  Widget build(BuildContext context) => FutureBuilder<int>(
    future: _count,
    builder: (context, snapshot) => Text(
      snapshot.hasError ? 'Students: unavailable' :
        snapshot.hasData ? 'Students: ${snapshot.data}' : 'Students: …',
      style: const TextStyle(color: Colors.grey, fontSize: 12),
    ),
  );
}
