from django.shortcuts import render,redirect
from django.views.generic import View
from notes import forms
from notes.forms import TaskForm,RegiterationForm
from notes.models import Task
from django.contrib import messages
from django import forms





class TaskCreateView(View):
    
    def get(self, request,*args,**kwargs):
        
        form_instance=TaskForm()
        
        return render(request, 'task_add.html',{"form":form_instance})
    
    def post(self, request, *args, **kwargs):
        
        form_instance = TaskForm(request.POST)
        
        print("-----------------------------------------")
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            print("============================================================= saved")
            
            messages.success(request, "task added successfully")
            
            return redirect("task-view")
        
        else:
            print("-------no--------------")
      
            messages.success(request, "task not added")
           
            return render(request, 'task_add.html', {"form": form_instance})
        
class TaskListView(View):
    
    def get(self, request,*args,**kwargs):
        
        # if not request.user.is_authenticated:
            
        #     # return redirect ("")
        search_text=request.GET.get("search_text")
        
        selected_category=request.GET.get("category","all")

        
        if search_text != None:
            
            # qs= Task.objects.filter(user=request.user)
            
            qs=Task.objects.filter(title__contains=search_text)
            
            # qs=qs.filter(Q(title__contains=search_text)|Q(description__contains=search_text)
            
        else:
            if selected_category == "all":
                # insted of all user=request.user
                
                qs=Task.objects.all()  
            else:
                qs=Task.objects.filter(category=selected_category)
                
                  # category=selected_category, after this give  user=request.user
                
        return render(request, 'task_view.html',{"tasks":qs,
                                                 "selected":request.GET.get("category","all")})
        
    
class BasepageView(View):
    
    def get(self, request,*args,**kwargs):
        
        form_instance=TaskForm()
        
        qs=Task.objects.all()
    
        return render(request, 'task_view.html')
    
class TaskDetailView(View):
    
    def get(self, request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=Task.objects.get(id=id)
    
        return render(request, 'task_detail.html',{"task":qs})
    
class TaskUpdateView(View):
    
    def get(self, request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=Task.objects.get(id=id)
        
        form_instance=TaskForm(instance=qs)
        
        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select" }),initial=qs.status)
            
        return render(request, 'task_edit.html',{"form":form_instance})
    
    def post(self, request, *args, **kwargs):
        
        id=kwargs.get("pk")
        
        taskobj=Task.objects.get(id=id)
        
        form_instance=TaskForm(request.POST,instance=taskobj)
        
        if form_instance.is_valid():
            
            form_instance.instance.status=request.POST.get("status")
            
            form_instance.save()
            
            return redirect("task-view")
        else:
            
            return render(request, 'task_edit.html',{"form":form_instance})
        
        # id=kwargs.get("pk")
        
        # qs=Task.objects.filter(id=id)
        
        # form_instance = TaskForm(request.POST)
        
        # print("-----------------------------------------")
        
        # if form_instance.is_valid():
            
        #     data=form_instance.cleaned_data
            
        #     status=request.POST.get("status")
            
        #     Task.objects.filter(id=id).update(**data,status=status)
            
        #     print("============================================================= saved")
            
        #     messages.success(request, "task updated successfully")
            
        #     return redirect("task-view")
        
        # else:
            
        #     return render(request, 'task_edit.html',{"form":form_instance})
        
class TaskDeleteView(View):
    
    def get(self, request,*args,**kwargs):
        
        Task.objects.get(id=kwargs.get("pk")).delete()
        
        return redirect("task-view")
    
from django.db.models import Count,Sum
class TaskSummaryView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=Task.objects.all()
        
        totaltask=qs.count()
        
        category_summary=Task.objects.all().values("category").annotate(Count("category"))
        print(category_summary)
        
        status_summary=Task.objects.all().values("status").annotate(Count("status"))
        print(status_summary)
        
        context={
            
            "totaltask":totaltask,
            "category_summary":category_summary,
            "status_summary":status_summary
            
        }
        
        return render(request,"task_summary.html",context)
    
    
class SignUpView(View):
    
    template_name="register.html"
    
    def get(self, request,*args,**kwargs):
        
        form_instance=RegiterationForm()
    
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self, request, *args, **kwargs):
        
        form_instance = RegiterationForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            print("============================================================= saved")
            
            messages.success(request, "sign in successfully")
            
            return redirect("task-view")
        else:
            
            print("-------no--------------")
      
            messages.success(request, "sign in  not successful")
           
        return render(request,self.template_name,{"form":form_instance})
    

 
    
    
