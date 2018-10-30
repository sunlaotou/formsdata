from django.shortcuts import render
from  django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from app01.models import *
# Create your views here.
class UserFrom(forms.Form):
    name = forms.CharField(min_length=2,error_messages={"required":"该字段不能为空"},
                           widget=widgets.TextInput(attrs={"class":"form-control"})
                           )
    pwd = forms.CharField(min_length=4,
                          error_messages={"required":"该字段不能为空"},
                          widget=widgets.PasswordInput(attrs={"class":"form-control"})
                          )
    r_pwd = forms.CharField(min_length=4,error_messages={"required":"该字段不能为空"},
                            widget=widgets.TextInput(attrs={"class":"form-control"})
                            )
    email = forms.EmailField(error_messages={"required":"该字段不能为空" ,"invalid":"格式错误"} ,widget=widgets.TextInput(attrs={"class":"form-control"})
                             )
    tel = forms.CharField(error_messages={"required":"该字段不能为空"},widget=widgets.TextInput(attrs={"class":"form-control"}))

    def clean_name(self):
        val = self.cleaned_data.get("name")
        res = formsdata.objects.filter(name=val)
        if not res:
            return val
        else:
            raise ValidationError("用户名已存在")
    def clean_tel(self):
        val =  self.cleaned_data.get("tel")
        if val ==11 :
            return val
        else: 
            raise ValidationError("手机格式不对")
    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")
        if pwd and r_pwd:
            if pwd ==r_pwd :
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


def index(request):

    if request.method=="POST":

        print(request.POST)

        #form=UserForm({"name":"yu","email":"123@qq.com","xxxx":"alex"})


        form=UserFrom(request.POST) # form表单的name属性值应该与forms组件字段名称一致

        print(form.is_valid()) # 返回布尔值

        if form.is_valid():
            print(form.cleaned_data)  # {"name":"yuan","email":"123@qq.com"}
        else:
            print(form.cleaned_data)  # {"email":"123@qq.com"}
            # print(form.errors)        # {"name":[".........."]}
            # print(type(form.errors))  # ErrorDict
            # print(form.errors. get("name"))
            # print(type(form.errors.get("name")))    # ErrorList
            # print(form.errors.get("name")[0])


            #   全局钩子错误
            #print("error",form.errors.get("__all__")[0])
            errors=form.errors.get("__all__")


            return render(request,"index.html",locals())

        '''

        form.is_valid()   :返回布尔值
        form.cleaned_data :{"name":"yuan","email":"123@qq.com"}
        form.errors       :{"name":[".........."]}

        '''


    form=UserFrom()

    return render(request,"index.html",locals())
