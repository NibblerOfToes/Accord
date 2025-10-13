function toggleFields() {
  const role = document.getElementById('role-select').value;
  const studentFields = document.getElementById('student-fields');
  const teacherFields = document.getElementById('teacher-fields');
  const groupSelect = document.getElementById('classLevel');
  const subjectInput = document.querySelector('input[name="subject"]');

  studentFields.style.display = role === 'student' ? 'block' : 'none';
  teacherFields.style.display = role === 'teacher' ? 'block' : 'none';

  if (role === 'student') {
    groupSelect.required = true;
    subjectInput.required = false;
  } else if (role === 'teacher') {
    groupSelect.required = false;
    subjectInput.required = true;
  } else {
    groupSelect.required = false;
    subjectInput.required = false;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  toggleFields();
  document.getElementById('role-select').addEventListener('change', toggleFields);
});