dermalink
=========

User side
------------
Diagnosis results inside specific issue page
User needs to edit profile
	cannot create issue until profile is 100% complete
		make a function that is called everytime they edit profile and if it is complete, update is_complete column in DB
	Get redirected to edit page if not complete



Derm side
------------
List outstanding issues
All resolved issues
Inside issue page
	form for diagnosing the issue
	display info for issue and patient and pictures
Doctors need to edit profile
	must be complete before they diagnos
		make a function that is called everytime they edit profile and if it is complete, update is_complete column in DB
	Get redirected to edit page if not complete

We need an algorithm for assigning issues to dermatologists
	Derms specify how many issues they want to handle at a time
	issues are replaced as soon as they are resolved
	round robin scheduling
	Doctor should not be able to hold onto an issue for a certain amount of time (eg 48 hours)