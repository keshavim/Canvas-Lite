


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from webapp.models import *
from webapp.models.users import UserType

def user_sections(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("/login")

    sections = user.get_sections()
    is_instructor = user.group_name == UserType.INSTRUCTOR

    main_sections_with_subsections = []
    if is_instructor:
        main_sections = user.get_main_sections()

        for main_section in main_sections:
            subsections = main_section.get_subsections()

            main_sections_with_subsections.append({
                'main_section': main_section,
                'subsections': subsections,
            })

    context = {
        'sections': sections,
        'is_instructor': is_instructor,
        'main_sections_with_subsections': main_sections_with_subsections,
    }
    return render(request, 'standard_pages/list_courses.html', context)

@login_required
def section_detail(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    is_subsection = section.is_sub_section()
    return render(request, 'standard_pages/section_detail.html', {
        'section': section,
        'is_subsection': is_subsection,
    })

@login_required
def manage_subsection_instructor(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    # Only allow assignment for subsections
    if not section.is_sub_section():
        return redirect('section_detail', section_id=section_id)

    # Get all TAs
    tas = User.objects.filter(groups__name='TA', is_active=True)

    # Filter TAs using your is_eligible method
    available_tas = [ta for ta in tas if ta.is_eligible(section)]

    if request.method == 'POST':
        ta_id = request.POST.get('ta_id')
        ta = get_object_or_404(User, id=ta_id)
        if ta.is_eligible(section):
            section.instructor = ta
            section.save()
        return redirect('section_detail', section_id=section.id)

    return render(request, 'standard_pages/assign_sections.html', {
        'section': section,
        'available_tas': available_tas,
        'previous_url': request.META.get('HTTP_REFERER', '/')
    })

@login_required
def assign_subsection_instructor(request, subsection_id, user_id):
    subsection = get_object_or_404(Section, id=subsection_id)

    # Verify permissions: current user is main section instructor
    if not subsection.main_section or subsection.main_section.instructor != request.user:
        return redirect('dashboard')

    new_instructor = get_object_or_404(User, id=user_id)

    # Verify new instructor is TA or self
    if new_instructor != request.user and not new_instructor.groups.filter(name='TA').exists():
        return redirect('dashboard')

    subsection.instructor = new_instructor
    subsection.save()

    return redirect('manage_subsection_instructors', section_id=subsection.main_section.id)


@login_required
def unassign_subsection_instructor(request, subsection_id):
    subsection = get_object_or_404(Section, id=subsection_id)

    # Verify permissions: current user is main section instructor
    if not subsection.main_section or subsection.main_section.instructor != request.user:
        return redirect('dashboard')

    subsection.instructor = None
    subsection.save()

    return redirect('manage_subsection_instructors', section_id=subsection.main_section.id)
