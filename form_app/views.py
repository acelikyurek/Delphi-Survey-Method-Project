from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AnswerQuestion, AnswerSheet, Form, Question
import numpy as np


def loginPage(request):

    error_given = False

    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            if error_given is False:
                messages.error(request, 'Username does not exist!')
                error_given = True

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            if error_given is False:
                messages.error(request, 'Username or password is incorrect!')
                error_given = True

    return render(request, 'login.html')


def logoutPage(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def mainPage(request):

    forms = Form.objects.all()
    forms = sorted(forms, key=lambda x: x.type_id)
    completed = []

    for form in forms:
        if AnswerSheet.objects.filter(form=form).filter(user=request.user):
            completed.append(True)
        else:
            completed.append(False)

    return render(request, 'main.html', {'listOfArgs': zip(forms, completed)})


@login_required(login_url='login')
def formPage(request, form_id):

    form = Form.objects.get(id=form_id)
    questions = list(Question.objects.filter(forms__id=form.id))
    questions = sorted(questions, key=lambda x: x.description)
    old_answers_user = []
    old_answers = []
    first_quartile = []
    median = []
    third_quartile = []
    iqr = []

    if AnswerSheet.objects.filter(form=form).filter(user=request.user):
        return redirect('main')

    if form.type_id != 1 and not AnswerSheet.objects.filter(form__type_id=form.type_id - 1).filter(user=request.user):
        return redirect('main')

    if form.type_id > 1:
        for i in questions:
            oldAnswerUser = AnswerQuestion.objects.filter(question=i).filter(
                answer_sheet__form__type_id=form.type_id - 1).filter(answer_sheet__user=request.user)
            if len(oldAnswerUser) == 0:
                old_answers_user.append('N/A')
            else:
                old_answers_user.append(oldAnswerUser[0].option)
            oldAnswer = AnswerQuestion.objects.filter(question=i).filter(
                answer_sheet__form__type_id=form.type_id - 1)
            old_answers.clear()
            for j in oldAnswer:
                old_answers.append(int(j.option))
            if len(old_answers) == 0:
                first_quartile.append('N/A')
                median.append('N/A')
                third_quartile.append('N/A')
                iqr.append('N/A')
            else:
                values = np.percentile(old_answers, [25, 50, 75])
                first_quartile.append("{:.2f}".format(values[0]))
                median.append("{:.2f}".format(values[1]))
                third_quartile.append("{:.2f}".format(values[2]))
                iqr.append("{:.2f}".format(values[2] - values[0]))
    else:
        for i in questions:
            old_answers_user.append('N/A')
            first_quartile.append('N/A')
            median.append('N/A')
            third_quartile.append('N/A')
            iqr.append('N/A')

    answers = []
    answerSheet = AnswerSheet(form=form, user=request.user)
    finished = False

    if request.method == 'POST':
        for i in questions:
            opt = request.POST.get(str(i.id), False)
            comment = request.POST.get(str(i.id) + " comment", "")
            if opt == False:
                messages.error(request, 'Please answer all the questions.')
                answers.clear()
                finished = False
                break
            else:
                answers.append(AnswerQuestion(
                    option=opt, comment=comment, question=i, answer_sheet=answerSheet))
                finished = True

        if finished == True:
            answerSheet.save()
            for j in answers:
                j.save()
            return redirect('main')

    return render(request, 'form.html', {'form': form, 'listOfArgs': zip(questions, old_answers_user, first_quartile, median, third_quartile, iqr)})


@login_required(login_url='login')
def statsPage(request):

    if not request.user.is_superuser:
        return redirect('main')

    forms_first = True
    for i in list(Form.objects.filter(type_id=1)):
        if i.visible == False:
            forms_first = False
            break
    if len(Form.objects.filter(type_id=1)) == 0:
        forms_first = False

    forms_second = True
    for i in list(Form.objects.filter(type_id=2)):
        if i.visible == False:
            forms_second = False
            break
    if len(Form.objects.filter(type_id=2)) == 0:
        forms_second = False

    forms_third = True
    for i in list(Form.objects.filter(type_id=3)):
        if i.visible == False:
            forms_third = False
            break
    if len(Form.objects.filter(type_id=3)) == 0:
        forms_third = False

    forms_fourth = True
    for i in list(Form.objects.filter(type_id=4)):
        if i.visible == False:
            forms_fourth = False
            break
    if len(Form.objects.filter(type_id=4)) == 0:
        forms_fourth = False

    forms_fifth = True
    for i in list(Form.objects.filter(type_id=5)):
        if i.visible == False:
            forms_fifth = False
            break
    if len(Form.objects.filter(type_id=5)) == 0:
        forms_fifth = False

    forms_sixth = True
    for i in list(Form.objects.filter(type_id=6)):
        if i.visible == False:
            forms_sixth = False
            break
    if len(Form.objects.filter(type_id=6)) == 0:
        forms_sixth = False

    users = list(User.objects.filter(is_superuser=False))
    users = sorted(users, key=lambda x: x.username)
    firsts = []
    seconds = []
    thirds = []
    fourths = []
    fifths = []
    sixths = []

    for i in users:
        if len(Form.objects.filter(type_id=1)) == 0:
            firsts.append(2)
        elif len(Form.objects.filter(type_id=1)) > len(AnswerSheet.objects.filter(form__type_id=1).filter(user=i)):
            firsts.append(1)
        else:
            firsts.append(0)

        if len(Form.objects.filter(type_id=2)) == 0:
            seconds.append(2)
        elif len(Form.objects.filter(type_id=2)) > len(AnswerSheet.objects.filter(form__type_id=2).filter(user=i)) or len(Form.objects.filter(type_id=2)) == 0:
            seconds.append(1)
        else:
            seconds.append(0)

        if len(Form.objects.filter(type_id=3)) == 0:
            thirds.append(2)
        elif len(Form.objects.filter(type_id=3)) > len(AnswerSheet.objects.filter(form__type_id=3).filter(user=i)) or len(Form.objects.filter(type_id=3)) == 0:
            thirds.append(1)
        else:
            thirds.append(0)

        if len(Form.objects.filter(type_id=4)) == 0:
            fourths.append(2)
        elif len(Form.objects.filter(type_id=4)) > len(AnswerSheet.objects.filter(form__type_id=4).filter(user=i)) or len(Form.objects.filter(type_id=4)) == 0:
            fourths.append(1)
        else:
            fourths.append(0)

        if len(Form.objects.filter(type_id=5)) == 0:
            fifths.append(2)
        elif len(Form.objects.filter(type_id=5)) > len(AnswerSheet.objects.filter(form__type_id=5).filter(user=i)) or len(Form.objects.filter(type_id=5)) == 0:
            fifths.append(1)
        else:
            fifths.append(0)

        if len(Form.objects.filter(type_id=6)) == 0:
            sixths.append(2)
        elif len(Form.objects.filter(type_id=6)) > len(AnswerSheet.objects.filter(form__type_id=6).filter(user=i)) or len(Form.objects.filter(type_id=6)) == 0:
            sixths.append(1)
        else:
            sixths.append(0)

    type_one = 2
    type_two = 2
    type_three = 2
    type_four = 2
    type_five = 2
    type_six = 2

    forms_one = Form.objects.filter(type_id=1)
    if len(forms_one) > 0:
        if forms_one[0].visible:
            type_one = 0
        else:
            type_one = 1

    forms_two = Form.objects.filter(type_id=2)
    if len(forms_two) > 0:
        if forms_two[0].visible:
            type_two = 0
        else:
            type_two = 1

    forms_three = Form.objects.filter(type_id=3)
    if len(forms_three) > 0:
        if forms_three[0].visible:
            type_three = 0
        else:
            type_three = 1

    forms_four = Form.objects.filter(type_id=4)
    if len(forms_four) > 0:
        if forms_four[0].visible:
            type_four = 0
        else:
            type_four = 1

    forms_five = Form.objects.filter(type_id=5)
    if len(forms_five) > 0:
        if forms_five[0].visible:
            type_five = 0
        else:
            type_five = 1

    forms_six = Form.objects.filter(type_id=6)
    if len(forms_six) > 0:
        if forms_six[0].visible:
            type_six = 0
        else:
            type_six = 1

    return render(request, 'stats.html', {'forms_first': forms_first, 'forms_second': forms_second, 'forms_third': forms_third, 'forms_fourth': forms_fourth, 'forms_fifth': forms_fifth, 'forms_sixth': forms_sixth, 'type_one': type_one, 'type_two': type_two, 'type_three': type_three, 'type_four': type_four, 'type_five': type_five, 'type_six': type_six, 'listOfArgs': zip(users, firsts, seconds, thirds, fourths, fifths, sixths)})


@login_required(login_url='login')
def formStatsPage(request, form_id):

    form = Form.objects.get(id=form_id)

    if not request.user.is_superuser:
        return redirect('main')

    if AnswerSheet.objects.filter(form=form).filter(user=request.user):
        return redirect('main')

    questions = list(Question.objects.filter(forms__id=form.id))
    questions = sorted(questions, key=lambda x: x.description)
    old_answers = []
    first_quartile = []
    median = []
    third_quartile = []
    iqr = []

    for i in questions:
        oldAnswer = AnswerQuestion.objects.filter(question=i).filter(
            answer_sheet__form__type_id=form.type_id)
        old_answers.clear()
        for j in oldAnswer:
            old_answers.append(int(j.option))
        if len(old_answers) == 0:
            first_quartile.append("N/A")
            median.append("N/A")
            third_quartile.append("N/A")
            iqr.append("N/A")
        else:
            values = np.percentile(old_answers, [25, 50, 75])
            first_quartile.append("{:.2f}".format(values[0]))
            median.append("{:.2f}".format(values[1]))
            third_quartile.append("{:.2f}".format(values[2]))
            iqr.append("{:.2f}".format(values[2] - values[0]))

    return render(request, 'formStats.html', {'form': form, 'listOfArgs': zip(questions, first_quartile, median, third_quartile, iqr)})


@login_required(login_url='login')
def openFormsPage(request, type_id):

    if not request.user.is_superuser:
        return redirect('main')

    forms = Form.objects.filter(type_id=type_id)
    for form in forms:
        form.visible = True
        form.save()

    return redirect('stats')


@login_required(login_url='login')
def closeFormsPage(request, type_id):

    if not request.user.is_superuser:
        return redirect('main')

    forms = Form.objects.filter(type_id=type_id)
    for form in forms:
        form.visible = False
        form.save()

    return redirect('stats')
