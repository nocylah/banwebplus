<?php
class semesterData {
	public static $name = 'Summer 2015';
	public static $subjects = array(
		'ACCT'=>'Accounting',
		'AE'=>'Aerospace Engineering',
		'AFAS'=>'Air Force Aerospace Studies',
		'ANTH'=>'Anthropology',
		'ART'=>'Art History',
		'BIOL'=>'Biology',
		'BA'=>'Business Administration',
		'BCS'=>'Business Computing Systems',
		'CERT'=>'Certifications',
		'CH E'=>'Chemical Engineering',
		'CHEM'=>'Chemistry',
		'CE'=>'Civil Engineering',
		'COMM'=>'Communication',
		'CED'=>'Community Education',
		'SVC'=>'Community Service',
		'CSE'=>'Computer Science & Engineering',
		'ERTH'=>'Earth Science',
		'ECON'=>'Economics',
		'EDUC'=>'Education',
		'EE'=>'Electrical Engineering',
		'EMGT'=>'Engineering Management',
		'ES'=>'Engineering Science',
		'ENGL'=>'English',
		'ENVE'=>'Environmental Engineering',
		'ENVS'=>'Environmental Science',
		'EXCH'=>'Exchange',
		'EXPL'=>'Explosives Engineering',
		'FIN'=>'Finance',
		'FA'=>'Fine Arts',
		'FREN'=>'French',
		'GEOC'=>'Geochemistry',
		'GEOL'=>'Geology',
		'GEOP'=>'Geophysics',
		'GERM'=>'German',
		'HW'=>'Health & Wellness',
		'HIST'=>'History',
		'HUMA'=>'Humanities',
		'HYD'=>'Hydrology',
		'IT'=>'Information Technology',
		'JAPN'=>'Japanese',
		'LIFE'=>'Lifestyle Activities',
		'MGT'=>'Management',
		'MKT'=>'Marketing',
		'MATE'=>'Materials Engineering',
		'MATH'=>'Mathematics',
		'MENG'=>'Mechanical Engineering',
		'METE'=>'Metallurgy',
		'MS'=>'Military Science',
		'ME'=>'Mineral Engineering',
		'MUS'=>'Music',
		'OPT'=>'Optics',
		'PETR'=>'Petroleum Engineering',
		'PHIL'=>'Philosophy',
		'PR'=>'Physical Recreation',
		'PHYS'=>'Physics',
		'PS'=>'Political Science',
		'PSY'=>'Psychology',
		'ST'=>'Science Teaching',
		'SS'=>'Social Science',
		'SPAN'=>'Spanish',
		'TC'=>'Technical Communication',
		'THEA'=>'Theater',
		'WGS'=>'Womens and Gender Studies',
	);
	public static $classes = array(
	);
	public static function to_json() {
		$a_retval = array('name'=>semesterData::$name, 'subjects'=>semesterData::$subjects, 'classes'=>semesterData::$classes);
		return json_encode($a_retval);
	}
}
?>