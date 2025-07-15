from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = ''
    initial_text = ''
    input_text = 'Cambiar imagen'
    template_name = 'widgets/custom_clearable_file_input.html'