from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Question, Field
from .forms import QuestionForm, FieldForm

def question_feed(request):
    if request.method == 'POST':
        # Handle field creation
        if 'create_field' in request.POST:
            field_form = FieldForm(request.POST)
            if field_form.is_valid():
                field_form.save()
                messages.success(request, 'Field created successfully!')
                return redirect('Questions:questions')
            else:
                messages.error(request, 'Error creating field. Please try again.')
        
        # Handle field deletion
        elif 'delete_field' in request.POST:
            field_id = request.POST.get('field_id')
            try:
                field = Field.objects.get(id=field_id)
                field_name = field.name
                field.delete()
                messages.success(request, f'Field "{field_name}" deleted successfully!')
            except Field.DoesNotExist:
                messages.error(request, 'Field not found.')
            except Exception as e:
                messages.error(request, f'Error deleting field: {str(e)}')
            return redirect('Questions:questions')
        
        # Handle question creation
        else:
            form = QuestionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Question created successfully!')
                return redirect('Questions:questions')
            else:
                messages.error(request, 'Error creating question. Please try again.')

    # Get all fields with question counts
    fields = Field.objects.all()
    field_data = []
    
    for field in fields:
        questions = Question.objects.filter(field=field)
        field_data.append({
            'field_id': field.id,
            'field_name': field.name,
            'field_slug': field.slug,
            'total': questions.count(),
            'advanced': questions.filter(level='Advanced').count(),
            'mid': questions.filter(level='Mid').count(),
            'beginner': questions.filter(level='Beginner').count(),
        })

    context = {
        'field_data': field_data,
        'question_form': QuestionForm(),
        'field_form': FieldForm(),
    }
    
    return render(request, 'admin/question_feed.html', context)


def edit_question(request, field_slug):
    field = get_object_or_404(Field, slug=field_slug)
    questions = Question.objects.filter(field=field)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print('post')
        if form.is_valid():
            print('data is valid')
            question = form.save(commit=False)
            question.field = field
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('Questions:edit_question', field_slug=field_slug)
    else:
        form = QuestionForm()

    context = {
        'field': field,
        'questions': questions,
        'form': form,
    }
    return render(request, 'admin/edit_question.html', context)

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # field_id = question.field.id
    question_text = question.question_text[:50]
    question.delete()
    messages.success(request, f'Question "{question_text}..." deleted successfully!')
    return redirect('Questions:edit_question', field_slug=question.field.slug)
