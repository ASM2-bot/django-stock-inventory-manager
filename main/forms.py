from django import forms
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity','Date']

    # ✅ Ces deux méthodes doivent être à l'intérieur de la classe
    def clean_category(self):
     category = self.cleaned_data.get('category')
     if not category:
        raise forms.ValidationError('This field is required.')
     return category 

    def clean_item_name(self): 
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name

# ✅ Aucun problème ici pour le formulaire de recherche


class StockSearchForm(forms.Form):
 

    category = forms.CharField(required=False, label="Category")
    item_name = forms.CharField(required=False, label="Item Name")
    export_to_CSV = forms.BooleanField(required=False)





class StockUpdateForm(forms.Form):
    category = forms.CharField(required=False, label="Category")
    item_name = forms.CharField(required=False, label="Item Name")
    quantity = forms.CharField(required=False, label="Quantity")


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['issue_quantity'].required = True
        self.fields['issue_to'].required = True
        
        # Add some basic validation
        self.fields['issue_quantity'].widget.attrs.update({
            'class': 'form-control',
            'min': '1'
        })
        self.fields['issue_to'].widget.attrs.update({
            'class': 'form-control'
        })
    
    def clean_issue_quantity(self):
        issue_quantity = self.cleaned_data.get('issue_quantity')
        if issue_quantity and issue_quantity <= 0:
            raise forms.ValidationError("Issue quantity must be greater than 0")
        return issue_quantity

















class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity']



class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']        