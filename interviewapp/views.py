from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
from datetime import datetime
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
#updation & deletion & insertion
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import QuestionsMaster
from django.template import loader
from django.urls import reverse
import json
from django.utils import timezone
from datetime import datetime 
from .models import show_user_result
from django.http import FileResponse
import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date

# Create your views here.

# home page
def homepage(request):      
     return render(request,'home_page.html')

 #showing the homepage  
def homepage1(request):
     return render(request,'home_page.html')

#showing the user details
def userpage(request):
    if 'username'in request.session and "usertype" in request.session:
        if request.session['usertype'] == '2':
            userdetails = registab.objects.get(Username=request.session['username'],fld_is_active=1)
            data = {
                "userdetails": userdetails
            }
            return render(request,'User_details.html', data)
        else:
            return redirect('logout')
    return redirect('logout')

#for the registered user
def show_registeruser(request):
     if 'username'in request.session and "usertype" in request.session:
        users=registab.objects.filter(is_deleted=0,fld_user_type_id=2).all().values()
        template=loader.get_template('register_user.html')
        context={
          'users':users,
                 }
        return HttpResponse(template.render(context,request))
     return redirect('login2')

#for download resume for the perticular user
def downloadfile(request, user_id):
    user = get_object_or_404(registab, fld_slno=user_id, fld_is_active=1)
    
    if user.File:
        file_path = user.File.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{user.File.name}"'
            return response
    else:
        return HttpResponse("No resume found for this user")
    
#for user and admin loginpage
def login2(request):
     if request.method == 'GET':
         return render(request,'login_page.html')
     if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        admin_user_db=registab.objects.filter(Username=username,password=password,fld_is_active=1,fld_user_type_id=1,is_deleted=0).exists()
        if admin_user_db:
            request.session['username'] = username
            request.session['usertype'] = '1'   
            return JsonResponse({"usertype": "1"})
        else:
            try:
                user_db=registab.objects.get(Username=username,password=password,fld_is_active=1,is_deleted=0)
            except registab.DoesNotExist:
                user_db = None
            if user_db:
                request.session['username'] = username
                request.session['usertype'] = '2'
                request.session['position'] = user_db.possition
                request.session['experience'] = user_db.Expereince
                request.session['fullname'] = user_db.full_name
                return JsonResponse({"usertype":"2"})
            else:
                return JsonResponse({"error": "Enter correct username and password !"})
        # user=registab.objects.filter(Username=Username,password=password,fld_is_active=1,fld_user_type_id=2).exists()
        # adminUser=registab.objects.filter(Username=Username,password=password,fld_is_active=1,fld_user_type_id=1).exists()
        # if user:
        #     userdetails = registab.objects.get(Username=Username,password=password,fld_is_active=1)
        #     fontend_data = {
        #         "userdetails": userdetails
        #     }
        #     request.session['Username'] = Username
        #     request.session['usertype'] = '2'
        #     request.session['position'] = userdetails.possition
        #     request.session['experience'] = userdetails.Expereince
        #     return JsonResponse({"error_msg": msg})
        # elif adminUser:
        #     mystudent = QuestionsMaster.objects.all()
        #     fontend_data = {
        #         "mystudent": mystudent
        #     }
        #     request.session['Username'] = Username
        #     request.session['usertype'] = '1'
        #     return render(request,'index.html', fontend_data)
        # else:
        #     data = {
        #         "error": True,
        #         "msg" : "Enter correct username and password!"
        #     }
        #     return render(request, 'login_page.html', data)
        #     # return JsonResponse({"login_status": "error", "error_msg": msg})
          
   
       
     return render(request,'login_page.html')
 

#For session logout
def logout(request):
    request.session.flush()
    return redirect('login2')

#return render(request,'login_page.html')
# Registration page
@csrf_exempt
def regspage(request):
    return render(request,'Registration_page.html')

#for user registration page
def register1(request):
    if request.method=='POST':
        full_name=request.POST['full_name']
        dateofbirth=request.POST['dateofbirth']
        gender=request.POST['gender']
        mobile_number=request.POST['mobile_number']
        email_id=request.POST['email_id']
        Expereince=request.POST['Expereince']
        possition=request.POST['possition']
        referd_by=request.POST['referd_by']
        home_town=request.POST['home_town'] 
        uploaded_resume = request.FILES.get('resume') 
        username=request.POST['Username']
        password=request.POST['password']
        c=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user=registab.objects.filter(Username=username, fld_is_active=1,is_deleted=0).exists()
        #print("user",user)
        
        if user:
            msg = "Username already exist!"
            return JsonResponse({"error_msg": msg})
        mobile_number_db=registab.objects.filter(mobile_number=mobile_number, fld_is_active=1,is_deleted=0).exists()
        if mobile_number_db:
            msg = "mobile number already exist!"
            return JsonResponse({"error_msg": msg})
        email_id_db=registab.objects.filter(email_id=email_id, fld_is_active=1,is_deleted=0).exists()
        if email_id_db:
            msg = "email id already exist!"
            return JsonResponse({"error_msg": msg})
        Rn = (registab.objects.all().values_list('fld_rn', flat=True).order_by('fld_rn').last())
        if Rn is None:
            Rn="1"
        else:
            Rn=(int(Rn)+1)
        Rf = (registab.objects.all().values_list('fld_rf_id', flat=True).order_by('fld_rf_id').last())
        if Rf is None:
            Rf="1"
        else:
            Rf=(int(Rf)+1)
        user=registab(fld_rn=Rn,fld_rf_id=Rf,full_name=full_name,dateofbirth=dateofbirth,gender=gender,
                      mobile_number=mobile_number,email_id=email_id,
                      Expereince= Expereince,possition=possition,referd_by=referd_by,
                      home_town=home_town,File=uploaded_resume,Username=username,password=password,fld_is_active=1,
                      modified_no="1",is_deleted=0,sys_insert_datetime=c,fld_user_type="user",
                      fld_user_type_id=2,attempts=0)
        user.save()
        #msg='sucessfully register'
        #return render(request,'Registration_page.html',{'Username':Username,'password':password})
        #return render(request,'userinfo.html',{'Fname':Fname,'Password':Password})
    return JsonResponse({"status": "success"})  


# for showing the instruction page
def instruction(request):
     if 'username'in request.session and "usertype" in request.session:
        return render(request,'instruction.html')
     return redirect('logout')

# TestResult
def testresult(request):
    return render(request,'TestResult.html')
  
   # adminlistview
def adminlv(request):
    return render(request,'adminList_view.html')

def userview(request):
    return render(request,'userview.html') 

from django.utils import timezone
from datetime import date, datetime, time


def admin_dashboard(request):
    if 'username' in request.session and 'usertype' in request.session:
        # Count the number of rows where fld_is_active is 1
        total_test = show_user_result.objects.filter(fld_is_active=1).count()
        # Count the number of rows where fld_is_active is 1 and fld_user_type_id is 2
        total_registered = registab.objects.filter(fld_is_active=1, fld_user_type_id=2).count()
        
        today = date.today()
        start_of_day = datetime.combine(today, time.min, tzinfo=timezone.get_current_timezone())
        end_of_day = datetime.combine(today, time.max, tzinfo=timezone.get_current_timezone())

        exams_today = show_user_result.objects.filter(
            fld_is_active=1,
            fld_sys_inserted_datetime__range=(start_of_day, end_of_day)
        ).count()

        return render(request, 'dashboard.html', {'total_test': total_test, 'total_registered': total_registered, 'exams_today': exams_today})
    
    return redirect('logout')


# for showing questions table
def index(request):
    if 'username' in request.session and 'usertype' in request.session:
        if request.session['usertype'] == '1':
            questions_master_db = QuestionsMaster.objects.filter(fld_is_deleted=0).all()

            # Process options to separate them by commas
            for question in questions_master_db:
                options = question.fld_option_name.split('$$')  # Split by dollar signs
                question.fld_option_name = ',  '.join(options)  # Join with commas

            data = {
                'questions_master_db': questions_master_db,
            }
            return render(request, 'index.html', data)
    else:
        return redirect('logout')

  
#for add questions and options
def add(request):
    if 'username' in request.session and 'usertype' in request.session:
        template = loader.get_template('Question_master.html')
        return HttpResponse(template.render({}, request))
    return redirect('logout')

#for add questions and options
def  addrecord(request):
  if 'username'in request.session and "usertype" in request.session:
    if request.method =='POST':
      experiences=request.POST['experience']
      positions=request.POST['position']
      questions=request.POST['question']
      options=request.POST.getlist('mytext')
      options = '$$'.join(options)
      correct_options=request.POST.get('correct_option')
      #input_str =options
      #values = input_str.split(',')
      #output = [i+1 for i in range(len(values))]
      #serialized_list = ','.join(map(str, output))  # Convert the list to a string
      c=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      Rn = (QuestionsMaster.objects.all().values_list('fld_rn', flat=True).order_by('fld_rn').last())
      if Rn is None:
            Rn="1"
      else:
            Rn=(int(Rn)+1)
      Rf = (QuestionsMaster.objects.all().values_list('fld_rf_id', flat=True).order_by('fld_rf_id').last())
      if Rf is None:
            Rf="1"
      else:
            Rf=(int(Rf)+1)
      qustion_number = (QuestionsMaster.objects.all().values_list('fld_question_number', flat=True).order_by('fld_question_number').last())
      if qustion_number is None:
         qustion_number="1"
      else:
         qustion_number=(int(qustion_number)+1)
      
      students=QuestionsMaster(fld_rn=Rn,fld_rf_id=Rf,fld_question_number= qustion_number,fld_total_exp_name=experiences,
                               fld_post_applied_for_name=positions,fld_sys_inserted_datetime=c,
                              fld_question_text=questions,fld_option_name=options, 
                              fld_correct_option_name=correct_options,fld_is_active=1, fld_is_deleted=0)
      students.save()
      return HttpResponseRedirect(reverse('index'))
      #return HttpResponse('Data Saved ')
    else:
        #return HttpResponse('Data not saved')
         return render(request,"Question_master.html")
  return redirect('logout')

#for delete the particular questions and options from the questions table
def delete(request,fld_slno):
  if 'username'in request.session and "usertype" in request.session:
    #questions_master_db=QuestionsMaster.objects.get(fld_slno=fld_slno)
    questions_master_db=QuestionsMaster.objects.get(fld_slno=fld_slno)
    questions_master_db.fld_is_deleted = 1
    questions_master_db.fld_deletion_datetime = timezone.now()
    questions_master_db.save()
    return HttpResponseRedirect(reverse('index'))
  return redirect('login2')

#for update questions table
def update(request,fld_slno):
  if 'username'in request.session and "usertype" in request.session:
    mystudent=QuestionsMaster.objects.get(fld_slno=fld_slno)
    template=loader.get_template('update.html')                            
    context={ 
        'mystudent':mystudent,
    }
    return HttpResponse(template.render(context,request))
  return redirect('logout')

def retun_page(request):
    if 'username' in request.session and 'usertype' in request.session:
        return render(request,'update.html')
    else:
        return redirect('logout')
    
# for update questions table
def updaterecord(request, fld_slno): 
    if 'username' in request.session and 'usertype' in request.session:                                                  
        if request.method == 'POST':
            experience = request.POST['experience']
            position = request.POST['position']
            question = request.POST['question']
            option = request.POST['mytext']
            correct_option = request.POST['correct_option']
            mystudent = QuestionsMaster.objects.get(fld_slno=fld_slno)
            mystudent.fld_total_exp_name = experience
            mystudent.fld_post_applied_for_name = position
            mystudent.fld_question_text = question
            mystudent.fld_option_name = option
            mystudent.fld_correct_option_name = correct_option
            mystudent.fld_modified_datetime = timezone.now()  # Update the modified date and time
            mystudent.save()
            return HttpResponseRedirect(reverse('index'))
    return redirect('logout')

# def updaterecord(request, fld_slno): 
#     if 'username' in request.session and 'usertype' in request.session:                                                  
#         if request.method == 'POST':
#             experience = request.POST['experience']
#             position = request.POST['position']
#             question = request.POST['question']
#             option1 = request.POST['option1']
#             option2 = request.POST['option2']
#             option3 = request.POST['option3']
#             option4 = request.POST['option4']
#             correct_option = request.POST['correct_option']
#             mystudent = QuestionsMaster.objects.get(fld_slno=fld_slno)
#             mystudent.fld_total_exp_name = experience
#             mystudent.fld_post_applied_for_name = position
#             mystudent.fld_question_text = question
#             mystudent.fld_option_name = '|'.join([option1, option2, option3, option4])
#             mystudent.fld_correct_option_name = correct_option
#             mystudent.fld_modified_datetime = timezone.now()
#             mystudent.save()
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             mystudent = QuestionsMaster.objects.get(fld_slno=fld_slno)
#             options = mystudent.fld_option_name.split('|')
#             context = {'mystudent': mystudent, 'options': options}
#             return render(request, 'update.html', context)
#     return redirect('logout')



#retriving questions and options from database
def stored_proc(request):
  if 'username'in request.session and "usertype" in request.session:
    cursor = connection.cursor()
    cursor.execute("call questions('{0}','{1}')".format(request.session['position'],request.session['experience']))
    results = cursor.fetchall()
    updated_results = []
    for row in results:
        options = row[3].split("$$") # split options field by dollar
        updated_row = (row[0], row[1], row[2], options) # create a new tuple with the updated options field
        updated_results.append(updated_row) # add the updated row to the list
    return render(request, 'Question_paper.html', {'QuestionsMaster': updated_results})
  else:
     return redirect('logout')



# def stored_proc(request):
#     if 'username' in request.session and 'usertype' in request.session:
#         # Assuming you have a 'username' key in the session that you are using later, uncomment the following line to print it for debugging purposes.
#         # print("request", request.session['username'])

#         position = request.session['position']
#         experience = request.session['experience']
      

#         # Assuming you have a 'user_id' or any other identifier to uniquely identify the user in your database
#         # attempts=attempts # Replace '123' with the actual user identifier from the session or wherever it's stored

#         try:
#             mystudent = registab.objects.filter(is_deleted=0).all().values()  # Retrieve the mystudent based on the 'user_id'
#             attempts = mystudent.attempts  # Get the 'attempts' field value from the retrieved mystudent object
#         except registab.DoesNotExist:
#             attempts = None  # If the mystudent doesn't exist, set attempts to None or handle the situation accordingly

#         if attempts is not None and attempts > 2:
#             # If attempts are more than two, redirect to 'logout' page
#             return redirect('logout')
#         else:
#             cursor = connection.cursor()
#             cursor.execute("call questions('{0}', '{1}')".format(position, experience))
#             results = cursor.fetchall()

#             updated_results = []
#             for row in results:
#                 options = row[3].split("$$")  # split options field by dollar
#                 updated_row = (row[0], row[1], row[2], options)  # create a new tuple with the updated options field
#                 updated_results.append(updated_row)  # add the updated row to the list

#             return render(request, 'Question_paper.html', {'QuestionsMaster': updated_results})
#     else:
#         return redirect('logout')

  


#calculating the user result and showing their result and stroing the user result also
def finalresult(request):
    if 'username' in request.session and 'usertype' in request.session:                  
        if request.method == 'POST':
            #session_details = request.session.items()
            #assement_user = request.session['username']
            assement_experince = request.session['experience']
            assement_position = request.session['position']
            assement_fullname = request.session['fullname']
            total_questions = int(request.POST['total_questions'])
            final_output = False
            answers = []
            correct_answers = []
            correct_answers_count = 0 
            percentage = 0

            if total_questions == 0:
                final_output = False
            else:
                final_output = True
                for i in range(1, total_questions + 1):
                    answers.append(request.POST.get(f'question{i}'))

                correc_answers_obj = QuestionsMaster.objects.filter(fld_is_deleted=0,fld_post_applied_for_name=request.session['position'], fld_total_exp_name=request.session['experience'])
                for capture_answers in correc_answers_obj:
                    correct_answers.append(capture_answers.fld_correct_option_name)

                for answer_index in range(total_questions):
                    if correct_answers[answer_index] == answers[answer_index]:
                        correct_answers_count += 1

                percentage = "{:.2f}".format(correct_answers_count / total_questions * 100)

            if final_output:

                # Save user result and answers
                for i in range(total_questions):
                    selected_option = answers[i]
                    correct_option = correct_answers[i]
                    question_text = correc_answers_obj[i]. fld_question_text  # Get the question text
                    current_datetime = datetime.now()
                    Rn = (trn_tbl_user_answered.objects.all().values_list('fld_rn_id', flat=True).order_by('fld_rn_id').last())
                    if Rn is None:
                       Rn="1"
                    else:
                       Rn=(int(Rn)+1)
                    Rf = (trn_tbl_user_answered.objects.all().values_list('fld_rf_id', flat=True).order_by('fld_rf_id').last())
                    if Rf is None:
                       Rf="1"
                    else:
                       Rf=(int(Rf)+1)
                    user_id = (trn_tbl_user_answered.objects.all().values_list('fld_user_id', flat=True).order_by('fld_user_id').last())
                    if  user_id is None:
                        user_id="1"
                    else:
                        user_id=(int(user_id)+1)
                    
                    user_result = trn_tbl_user_answered.objects.create(
                        fld_user_answer_name=selected_option,
                        fld_correct_option_name=correct_option,
                        fld_user_name=assement_fullname,
                        fld_experience=assement_experince,
                        fld_post_applied_for_name=assement_position,
                        fld_user_result=correct_answers_count,
                        fld_user_percentage=percentage,
                        fld_is_active=1,
                        fld_is_deleted=0,
                        fld_question_text=question_text,  # Save the question text in the database
                        fld_sys_inserted_datetime=current_datetime, # Save the current system time in the database
                        fld_rn_id=Rn,
                        fld_rf_id=Rf,
                        fld_user_id=user_id,
                        fld_total_mark = total_questions
                    )
                    user_result.save()

                current_user_db = registab.objects.get(Username=request.session['username'])
                current_user_db.attempts += 1
                current_user_db.save()

                Rn = (show_user_result.objects.all().values_list('fld_rn_id', flat=True).order_by('fld_rn_id').last())
                if Rn is None:
                    Rn="1"
                else:
                    Rn=(int(Rn)+1)
                Rf = (show_user_result.objects.all().values_list('fld_rf_id', flat=True).order_by('fld_rf_id').last())
                if Rf is None:
                       Rf="1"
                else:
                    Rf=(int(Rf)+1)
                user_id = (show_user_result.objects.all().values_list('fld_user_id', flat=True).order_by('fld_user_id').last())
                if  user_id is None:
                    user_id="1"
                else:
                    user_id=(int(user_id)+1)
                    

                result = show_user_result.objects.create(
                        fld_user_name=assement_fullname,
                        fld_experience=assement_experince,
                        fld_post_applied_for_name=assement_position,
                        fld_user_result=correct_answers_count,
                        fld_user_percentage=percentage,
                        fld_is_active=1,
                        fld_is_deleted=0,
                        fld_sys_inserted_datetime=current_datetime, # Save the current system time in the database
                        fld_rn_id=Rn,
                        fld_rf_id=Rf,
                        fld_user_id=user_id,
                        fld_total_mark = total_questions
                    )
                result.save()

                frontend_data = {
                    'correct_answers_count': correct_answers_count,
                    'total_questions': total_questions,
                    'percentage': percentage,
                    'userdetails': current_user_db
                }

                return render(request, 'Test_result.html', frontend_data)
    else:
        return redirect('logout')
    
#showing user result
def user_result(request):
     if 'username' in request.session and 'usertype' in request.session:                  
        result=show_user_result.objects.filter(fld_is_deleted=0).all().values()
        template=loader.get_template('user_result.html')
        context={
          'result':result,
                 }
        return HttpResponse(template.render(context,request))
     return redirect('logout')

def total_test(request):
    if 'username' in request.session and 'usertype' in request.session:
        result = show_user_result.objects.filter(fld_is_deleted=0,fld_is_active=1).all().values()
        # Count the number of rows where fld_is_active is 1
        total_test = show_user_result.objects.filter(fld_is_active=1).count()
        # Count the number of rows where fld_is_active is 1 and fld_user_type_id is 2

        today = date.today()
        start_of_day = datetime.combine(today, time.min, tzinfo=timezone.get_current_timezone())
        end_of_day = datetime.combine(today, time.max, tzinfo=timezone.get_current_timezone())
        users=registab.objects.filter(is_deleted=0,fld_user_type_id=2).all().values()

        exams_today = show_user_result.objects.filter(
            fld_is_active=1,
            fld_sys_inserted_datetime__range=(start_of_day, end_of_day)
        ).count()

        template = loader.get_template('total_test.html')
        context = {
            'result': result,
            'total_test': total_test,
            'exams_today': exams_today,
            'users':users,
        }
        return HttpResponse(template.render(context, request))
    
    return redirect('logout')

from django.shortcuts import render, redirect
from .models import show_user_result
from datetime import date, datetime, time
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

def today_test(request):
    if 'username' in request.session and 'usertype' in request.session:
      
        # Count the number of rows where fld_is_active is 1
        total_test = show_user_result.objects.filter(fld_is_active=1).count()
        today = date.today()
        start_of_day = datetime.combine(today, time.min, tzinfo=timezone.get_current_timezone())
        end_of_day = datetime.combine(today, time.max, tzinfo=timezone.get_current_timezone())
        exams_today = show_user_result.objects.filter(
            fld_is_active=1,
            fld_sys_inserted_datetime__range=(start_of_day, end_of_day)
        ).count()

        # Filter records for today's date
        exams_today_data = show_user_result.objects.filter(
            fld_is_active=1,
            fld_sys_inserted_datetime__range=(start_of_day, end_of_day)
        ).values()

        template = loader.get_template('today_test.html')
        context = {
            'exams_today': exams_today,
            'total_test': total_test,
            'exams_today_data':  exams_today_data,
        }
        return HttpResponse(template.render(context, request))
    
    return redirect('logout')
