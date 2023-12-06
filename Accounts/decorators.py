from functools import wraps
from django.shortcuts import redirect
from .models import User_Rolls, User_Details, candidate_details

def can_access_candidate_profile(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        userid = request.user.id

        # Check if the user is authenticated and has the required roles
        if request.user.is_authenticated:
            try:
                role = User_Rolls.objects.get(user_id=userid)
                # Assuming you have a "role" attribute in your User model
                if role.roll_id == 2:
                    return view_func(request, *args, **kwargs)
                if role.roll_id == 1:
                    return view_func(request, *args, **kwargs)
                if role.roll_id == 0:
                    email = kwargs.get('email')
                    print(email)
                    user_details = candidate_details.objects.get(id=userid)
                    print(request.user.email)
                    if request.user.email == email:
                        return view_func(request, *args, **kwargs)
            except User_Rolls.DoesNotExist:
                pass
        else:
            return redirect('signIn')

        # Redirect to an unauthorized page or raise a PermissionDenied exception
        return redirect('unauthorized')         

    return _wrapped_view
