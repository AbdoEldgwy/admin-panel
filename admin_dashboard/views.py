from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from .models import Dashboard
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def dashboard(request):
    all_data = Dashboard.objects.filter(created_by=request.user)
    # GET Filters
    selected_field = request.GET.get('field')
    selected_status = request.GET.get('status')

    if selected_field:
        all_data = all_data.filter(fields=selected_field)

    if selected_status:
        all_data = all_data.filter(status=selected_status)

    # unique values
    unique_fields = Dashboard.objects.values_list('fields', flat=True).distinct()
    unique_statuses = Dashboard.objects.values_list('status', flat=True).distinct()

    paginator = Paginator(all_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'dashboard_data': page_obj,
        'unique_fields': unique_fields,
        'unique_statuses': unique_statuses,
        'selected_field': selected_field,
        'selected_status': selected_status,
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
@login_required
def candidate(request):
    dashboard = Dashboard.objects.filter(created_by=request.user)

    # فلترة البحث بالكلمة المفتاحية
    search_query = request.GET.get('search', '')
    if search_query:
        dashboard = dashboard.filter(
            Q(name__icontains=search_query) |
            Q(mail__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # فلترة (field)
    selected_field = request.GET.get('field')
    if selected_field:
        dashboard = dashboard.filter(fields=selected_field)

    # فلترة (status)
    selected_status = request.GET.get('status')
    if selected_status:
        dashboard = dashboard.filter(status=selected_status)

    # unique values
    unique_fields = Dashboard.objects.values_list('fields', flat=True).distinct()
    unique_statuses = Dashboard.objects.values_list('status', flat=True).distinct()

    # Pagination
    paginator = Paginator(dashboard, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'dashboard': page_obj,
        'search_query': search_query,
        'unique_fields': unique_fields,
        'unique_statuses': unique_statuses,
        'selected_field': selected_field,
        'selected_status': selected_status,
    }
    return render(request, 'admin/candidate_admin.html', context)

@login_required
def candidate_details(request, slug):
    candidate = get_object_or_404(Dashboard, slug=slug, created_by=request.user)
    return render(request, 'admin/candidate_details.html', {'candidate': candidate})


@require_POST
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Dashboard, id=candidate_id, created_by=request.user)
    
    try:
        # Update candidate fields
        candidate.name = request.POST.get('name', candidate.name)
        candidate.mail = request.POST.get('mail', candidate.mail)
        candidate.phone = request.POST.get('phone', candidate.phone)
        candidate.fields = request.POST.get('fields', candidate.fields)
        candidate.status = request.POST.get('status', candidate.status)
        candidate.evaluation_point = request.POST.get('evaluation_point', candidate.evaluation_point)
        
        # Handle file uploads if provided
        if 'image' in request.FILES:
            candidate.image = request.FILES['image']
        if 'cv' in request.FILES:
            candidate.cv = request.FILES['cv']
            
        candidate.save()
        return JsonResponse({'status': 'success', 'message': 'Candidate updated successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
def delete_candidate(request, candidate_id):
    try:
        candidate = get_object_or_404(Dashboard, id=candidate_id, created_by=request.user)
        candidate.delete()
        return redirect('AdminDashboard:admin_dashboard')
    except Dashboard.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Candidate not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@require_POST
def delete_selected_candidates(request):
    selected_ids = request.POST.getlist('selected_ids')
    
    if selected_ids:
        Dashboard.objects.filter(id__in=selected_ids).delete()
        messages.success(request, f"{len(selected_ids)} candidate(s) deleted successfully.")
    else:
        messages.warning(request, "No candidates selected.")

    return redirect('AdminDashboard:admin_dashboard')