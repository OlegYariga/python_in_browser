from django.forms import ModelForm
from .models import Student, Test, Question, Answer, StudentTests
from django import forms


class RegistrationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name', 'status', 'group']

    def saveuser(self):
        user = self.save(commit=False)
        user.email = user.username
        user.set_password(self.cleaned_data['password'])
        user.save()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('test',)

    def set_new_questions_by_test(self, test_id, post_data):
        questions_list = ([post_data.get(str(k) + '-question') for k in range(1, 11)])
        answer_list = ([post_data.getlist(str(k) + '-answer') for k in range(1, 11)])
        check_list = ([post_data.getlist(str(k) + '-check') for k in range(1, 11)])
        question_obj_list = [Question(test=test_id, question=q) for q in questions_list]

        [q_obj.save() for q_obj in question_obj_list]
        for k, a_list in enumerate(answer_list):
            for z, a in enumerate(a_list):
                if str(z+1) in check_list[k]:
                    Answer(question=question_obj_list[k], answer=a, is_correct=True).save()
                else:
                    Answer(question=question_obj_list[k], answer=a).save()
        return True


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('question',)

    def select_related_questions(self, test_id):
        questions = Question.objects.filter(test__id=test_id)
        answers = Answer.objects.filter(question__in=questions)
        return questions, answers

    def check_answers(self, test_id, post_data, username):
        questions = Question.objects.filter(test__id=test_id)
        answers = Answer.objects.filter(question__in=questions, is_correct=True)
        user_answer_list = ([{question.id: post_data.getlist(str(question.id)+'-module_name')} for question in questions])
        list_of_questions = [{question.id: [answer.answer for answer in answers if answer.question == question]}
                             for question in questions]

        user_score = 0
        itog_list_of_questions = list()
        for u_ans in user_answer_list:
            for r_ans in list_of_questions:
                for ukey in u_ans.keys():
                    for rkey in r_ans.keys():
                        if ukey == rkey and u_ans.get(ukey) == r_ans.get(rkey):
                            itog_list_of_questions.append(Question.objects.filter(id=ukey).first())
                            user_score += 1
        result = user_score/questions.count()*100

        student_test = StudentTests.objects.filter(tests__id=test_id, user__username=username).first()
        if student_test:
            student_test.score = result
            student_test.save()
        else:
            if not Student.objects.filter(username=username).first():
                return 0, 0
            st = StudentTests(user=Student.objects.filter(username=username).first(), score=result)
            st.save()
            st.tests.add(Test.objects.filter(id=test_id).first())
            st.save()
        return result, itog_list_of_questions


class GroupViewForm(forms.Form):
    group = forms.IntegerField(label='Номер группы')

    def select_related_students(self, group):
        tests = Test.objects.all()
        if group:
            students = Student.objects.filter(group=group)
        else:
            students = Student.objects.all()
        student_tests = StudentTests.objects.filter(user__in=students)
        return tests, students, student_tests

