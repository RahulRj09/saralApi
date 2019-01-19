import requests
import json
import pathlib
import os
courses_id = []
file = pathlib.Path("courses.json")
def coursesdata():
	url='http://saral.navgurukul.org/api/courses'
	courses = requests.get(url)	
	with open("courses.json", "wb") as f:
		f.writelines(courses.iter_lines())

def openjsonfile():
	f = open("courses.json","r")
	data = f.read()
	coursesdata = json.loads(data)
	coursesdata = coursesdata['availableCourses']
	for i in range(0,len(coursesdata)):
		name = coursesdata[i]
		print i,name['name']
		courses_id.append(name['id'])


def debug(courses_id,filename):
	exercises_url = 'http://saral.navgurukul.org/api/courses/{}/exercises'.format(courses_id)
	exercise_courses = requests.get(exercises_url)
	with open(filename, "wb") as f:
		f.writelines(exercise_courses.iter_lines())

def slug(exercisedata,courses_id):
	slug = []
	print '\tchildExercises'
	for i in range(0,len(exercisedata)):
		childExercises = exercisedata[i]
		if childExercises['childExercises'] == []:
			pass
		else:
			name=childExercises['childExercises']
			print '\t\t',i,name[0]['name']
		slug.append(childExercises['slug'])
	for i in range(len(slug)):
		print i,slug[i]
	slugid = input("enter slug id")
	slugid = slug[slugid]
	urldemo = "http://saral.navgurukul.org/api/courses/{}/exercise/getBySlug?slug={}".format(courses_id,slugid)
	dataslug = requests.get(urldemo).text
	# dataslug = json.dumps(dataslug)
	print(dataslug) 

def openfile(courses_id,user_selectcourse):
	courses_id = courses_id[user_selectcourse]
	slugcoures_id = courses_id
	filename ="exercise_"+str(courses_id)+".json"
	filepath = pathlib.Path(filename)
	if filepath.exists():
		pass
	else:
		debug(courses_id,filename)
	exercisesdata = open(filename,"r")
	exercisesdata = exercisesdata.read()
	exercisesdata = json.loads(exercisesdata)
	exercisedata = exercisesdata['data']
	return exercisedata , slugcoures_id
if file.exists():
	pass
else:
	coursesdata()
openjsonfile()

user_selectcourse = input("Enter courses number")
exercisedata , slugcoures_id = openfile(courses_id,user_selectcourse)
 
slug(exercisedata,slugcoures_id)



while True:
	user = raw_input("Enter Your choice \n 'Up show all courses' \n 'P Previous exercise' \n 'N next exercise'")
	if user == 'Up':
		openjsonfile()
	elif user == 'P':
		user_selectcourse -=1
		exercisedata , slugcoures_id = openfile(courses_id,user_selectcourse)
		slug(exercisedata,slugcoures_id)
	elif user == 'N':
		user_selectcourse +=1
		exercisedata , slugcoures_id = openfile(courses_id,user_selectcourse)
		slug(exercisedata,slugcoures_id)