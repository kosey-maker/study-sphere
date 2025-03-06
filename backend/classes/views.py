from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Class, ClassMembership, Educator, Student

def create_class(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_datetime = request.POST.get('class_datetime')
        
        try:
            class_datetime = datetime.strptime(class_datetime, '%Y-%m-%d %H:%M')
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Use this format: YYYY-MM-DD HH:MM.'}, status=400)
        
        educator = Educator.objects.get(user=request.user)
        new_class = Class.objects.create(name=name, educator=educator, class_datetime=class_datetime)
        return JsonResponse({'status': 'success', 'class_id': new_class.id})

def delete_class(request, class_id):
    if request.method == 'POST':
        class_instance = get_object_or_404(Class, id=class_id)

        if request.user != class_instance.educator.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        class_instance.delete()
        return JsonResponse({'status': 'success', 'message': 'Class deleted successfully.'})
    
def request_to_join(request, class_id):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        class_instance = get_object_or_404(Class, id=class_id)
        
        if ClassMembership.objects.filter(student=student, class_instance=class_instance).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already requested to join this class.'}, status=400)
        
        ClassMembership.objects.create(student=student, class_instance=class_instance)
        return JsonResponse({'status': 'success', 'message': 'Join request sent.'})

    
 #educator accept the request to join or no

def joinrequest(request, membership_id): 
    if request.method == 'POST':
        membership = get_object_or_404(ClassMembership, id=membership_id)
        class_instance = membership.class_instance

        if request.user != class_instance.educator.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        action = request.POST.get('action')
        if action == 'accept':
            membership.is_accepted = True
            membership.save()
            return JsonResponse({'status': 'success', 'message': 'Request accepted.'})
        elif action == 'reject':
            membership.delete()
            return JsonResponse({'status': 'success', 'message': 'Request rejected.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)

    

# educator have permission to remove any student from his class 
    def remove_student(request, class_id, student_id):
     if request.method == 'POST':
        
        class_instance = get_object_or_404(Class, id=class_id)
        educator = Educator.objects.get(user=request.user)
        
        if class_instance.educator != educator:
            return JsonResponse({'status': 'error', 'message': 'You do not have the permission.'}, status=403)
        
        student = get_object_or_404(Student, id=student_id)
        
        ClassMembership.objects.filter(class_instance=class_instance, student=student).delete()
        return JsonResponse({'status': 'success', 'message': 'Student removed from class.'})
     

     # function give the calss
     def get_class(request, class_id):
      if request.method == 'GET':
        
        class_instance = get_object_or_404(Class, id=class_id)
        
       
        return JsonResponse({
            'status': 'success',
            'class_id': class_instance.id,
            'name': class_instance.name,
            'educator': class_instance.educator.user.username,
            'class_datetime': class_instance.class_datetime.strftime('%Y-%m-%d %H:%M'),
            'students': [student.user.username for student in class_instance.students.all()]   
        })