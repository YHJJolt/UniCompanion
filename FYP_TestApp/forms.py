from django import forms
from .models import *

#Signup / Login Page
class SignupForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        min_length=5,
        max_length=20,
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus',
            'placeholder': 'John Doe',
            'id': 'username'
        })
    )

    stu_email = forms.EmailField(
        required=True,
        label="Student Email",
        widget=forms.EmailInput(attrs={
            "class": "w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus",
            "placeholder": "...@student.newinti.edu.my",
            'id': 'signupEmail'
        })
    )

    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus',
            'placeholder': '••••••••',
            'id': 'signupPassword'
        })
    )

    confirmpassword = forms.CharField(
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus',
            'placeholder': '••••••••',
            'id': 'confirmPassword'
        })
    )

    class Meta:
        model = Users
        fields = ['username', 'stu_email', 'password']

    def clean(self):
        print(super().clean())
        cleaned_data = super().clean()
        password = cleaned_data.get('signupPassword')
        confirm_password = cleaned_data.get('confirmPassword')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        # Check if the passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

#Login Form / Page
class LoginForm(forms.ModelForm):
    stu_email = forms.EmailField(
        required=True,
        label="Student Email",
        widget=forms.EmailInput(attrs={
            "class": "w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus",
            "placeholder": "...@student.newinti.edu.my",
            'id': 'loginEmail'
        })
    )

    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-3 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-purple-500 input-focus',
            'placeholder': '••••••••',
            'id': 'loginPassword'
        })
    )

    class Meta:
        model = Users
        fields = ['stu_email', 'password']

#Home Post Form
class PostForm(forms.ModelForm):
    flair = forms.ModelChoiceField(  # Use ModelChoiceField for single selection
        queryset=Flair.objects.all(),
        label="Flair",
        empty_label='Select Flairs',
        widget=forms.Select(
            attrs = {
                "class": 'px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50',
            })
    )

    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={
            'class': "w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker",
            'placeholder': 'Please enter your title...',
        })
    )

    description = forms.CharField(
        required=True,
        label="Description",
        widget=forms.Textarea(attrs={
            'class': "w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker",
            'placeholder': 'Your content goes here...',
        })
    )

    class Meta:
        model = Posts
        fields = ['flair', 'title', 'description']

# Indiv Post Comment
class IndivPostCommentForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        label="Add a Comment",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none foul-checker',
            'rows': '4',
            'placeholder': 'Share your thoughts...',
            'id': 'commentTextarea',
        })
    )

    class Meta:
        model = PostComments
        fields = ['content']

# Search bar
class SearchForm(forms.Form):
    searchQuery = forms.CharField(
        required=True,
        label="Search",
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker',
            'placeholder': 'Search...',
            'id': 'searchForm',
        })
    )

#Events / Calendar Page
class EventForm(forms.ModelForm):
    category = forms.ChoiceField(
        required=True,
        label="Category",
        choices=[
            ('Academic', 'Academic'),
            ('Assignment', 'Assignment'),
            ('Extracurricular', 'Extracurricular'),
            ('Personal', 'Personal'),
            ('Study', 'Study'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            "class": 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'id': 'eventCategory'
        })
    )

    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Event Title',
            'id': 'eventTitle'
        })
    )

    date = forms.DateField(
        required=True,
        label= "Date",
        widget=forms.DateInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'date',
            'id': 'eventDate'
        })
    )

    start_time = forms.TimeField(
        required=True,
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'time',
            'id': 'eventStartTime'
        })
    )

    end_time = forms.TimeField(
        required=True,
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'time',
            'id': 'eventEndTime'
        })
    )

    location = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Where is the event?',
            'id': 'eventLocation'
        })
    )

    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Event Description',
            'id': 'eventDescription',
            'rows': 4
        })
    )

    color_Choices = [
        ('bg-blue-500', 'Blue'),
        ('bg-purple-500', 'Purple'),
        ('bg-green-500', 'Green'),
        ('bg-yellow-500', 'Yellow'),
        ('bg-red-500', 'Red'),
        ('bg-indigo-500', 'Indigo'),
        ('bg-pink-500', 'Pink'),
        ('bg-teal-500', 'Teal'),
    ]

    color = forms.ChoiceField(
        required=False,
        label="Color",
        choices=color_Choices,
        widget=forms.Select(attrs={
            'class': 'hidden',
            'id': 'eventColor'
        })
    )


    class Meta:
        model = CalendarEvent
        fields = ['category', 'title']

#Events Edit Form
class EventEditForm(forms.ModelForm):
    category = forms.ChoiceField(
        required=True,
        label="Category",
        choices=[
            ('Academic', 'Academic'),
            ('Assignment', 'Assignment'),
            ('Extracurricular', 'Extracurricular'),
            ('Personal', 'Personal'),
            ('Study', 'Study'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            "class": 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'id': 'eventCategory'
        })
    )

    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Event Title',
            'id': 'eventTitle'
        })
    )

    date = forms.DateField(
        required=True,
        label="Date",
        widget=forms.DateInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'date',
            'id': 'eventDate'
        })
    )

    start_time = forms.TimeField(
        required=True,
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'time',
            'id': 'eventStartTime'
        })
    )

    end_time = forms.TimeField(
        required=True,
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'type': 'time',
            'id': 'eventEndTime'
        })
    )

    location = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Where is the event?',
            'id': 'eventLocation'
        })
    )

    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Event Description',
            'id': 'eventDescription',
            'rows': 4
        })
    )

    color_Choices = [
        ('bg-blue-500', 'Blue'),
        ('bg-purple-500', 'Purple'),
        ('bg-green-500', 'Green'),
        ('bg-yellow-500', 'Yellow'),
        ('bg-red-500', 'Red'),
        ('bg-indigo-500', 'Indigo'),
        ('bg-pink-500', 'Pink'),
        ('bg-teal-500', 'Teal'),
    ]

    color = forms.ChoiceField(
        required=False,
        label="Color",
        choices=color_Choices,
        widget=forms.Select(attrs={
            'class': 'hidden',
            'id': 'eventColor'
        })
    )

    class Meta:
        model = CalendarEvent
        fields = ['category', 'title']

#Profile Page
class ProfileForm(forms.ModelForm):
    votes = forms.ChoiceField(
        required=True,
        label="Votes",
        choices= [
            ('upvote', 'Upvote'),
            ('downvote', 'Downvote'),
        ],
        widget=forms.Select(attrs={
            'class': 'hidden',
            'id': 'eventVotes'
    }))

    profile_feedback = forms.CharField(
        required=True,
        label="Community Feedback",
        widget=forms.Textarea(attrs={
            'class': "w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker",
            'placeholder': "Share your thoughts...",
            'id': "comment-text",
            'rows': "4",
        }))

    class Meta:
        model = UserComments
        fields = ['profile_feedback']

#Edit Profile Page
class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        min_length=5,
        max_length=20,
        required=True,
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker',
            'placeholder': 'Username',
            'id': 'edit-name'
    }))

    description = forms.CharField(
        required=False,
        label="Bio",
        widget=forms.Textarea(attrs={
            'class': "block w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 foul-checker",
            'placeholder': "Enter something for your bio...",
            'id': "edit-bio",
            'rows': "4",
        }))

    class Meta:
        model = Users
        fields = ['description']  # having the username here made the form think that we're creating a user,

#EditProfileImageForm
class EditProfileImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'id': "main-photo-upload",
        }))
    class Meta:
        model = Users
        fields = ['image']

#Saved Page
# class SavesForm(forms.ModelForm):
#     saved_posts = forms.CharField(
#         required=False,
#         label="Saved Posts",
#         widget=forms.Textarea(attrs={
#
#         })
#     )

#Companion AI
class CompanionForm(forms.ModelForm):
    companion_name = forms.CharField(
        required=False,
        label="Companion Name",
        widget=forms.TextInput(attrs={

        })
    )

    companion_desc = forms.CharField(
        required=False,
        label="Companion Description",
        widget=forms.Textarea(attrs={

        })
    )

    companion_chat_session = forms.CharField(
        required=False,
        label="Companion Chat Session",
        widget=forms.Textarea(attrs={

        })
    )

    companion_messages = forms.CharField(
        required=False,
        label="Companion Messages",
        widget=forms.Textarea(attrs={

        })
    )

#Admin Dashboard


#Reported Content

#Flair
class EditFlairForm(forms.ModelForm):
    flair_name = forms.CharField(
        max_length=15,
        required=True,
        label="Flair Name",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Please enter a flair name...',
            'id': 'flair-name',
            }))

    color_Choices = [
        ('bg-red-500', '🔴 Red'),
        ('bg-orange-500', '🟠 Orange'),
        ('bg-yellow-500', '🟡 Yellow'),
        ('bg-green-500', '🟢 Green'),
        ('bg-blue-500', '🔵 Blue'),
        ('bg-purple-500', '🟣 Purple'),
    ]

    flair_color = forms.ChoiceField(
        required=True,
        label="Flair Color",
        choices=color_Choices,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'flair-color',
        })
    )

    class Meta:
        model = Flair
        fields = ['flair_name', 'flair_color']

#Chatbot FAQ Setup
class AddFAQForm(forms.ModelForm):
    category = forms.ModelChoiceField(  # Use ModelChoiceField for single selection
        queryset=CompanionFAQCategory.objects.all(),
        label="Category *",
        empty_label='Select Category',
        widget=forms.Select(
            attrs={
                "class": 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500',
                'id': 'faqCategory'
            })
    )

    question = forms.CharField(
        required=True,
        label="Question *",
        widget=forms.Textarea(attrs={
            'class': "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500",
            'rows': "3",
            'placeholder': 'Enter the question...',
            'id': 'question',
        })
    )

    answer = forms.CharField(
        required=True,
        label="Answer *",
        widget=forms.Textarea(attrs={
            'class': "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500",
            'rows': "3",
            'placeholder': 'Enter the answer...',
            'id': 'answer',
        })
    )

    keywords = forms.CharField(
        required=True,
        label="Keywords *",
        widget=forms.Textarea(attrs={
            'class': "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500",
            'rows': "3",
            'placeholder': 'help, faq, menu, etc...',
            'id': 'keywords',
        })
    )

    class Meta:
        model = CompanionFAQ
        fields = ['category', 'question', 'answer', 'keywords']
