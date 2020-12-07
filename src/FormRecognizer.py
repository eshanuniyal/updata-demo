import csv
import pair_data

class FormRecognizer:

	endpoint = "https://ctrlzrecognition.cognitiveservices.azure.com/"
	api_key = "dea887218b724549bebe8b4e0ce48aa0"
	# model_id = "e836618c-0066-490d-85ab-a4fe6a664d4d"  # v1+3
	model_id = "569932ce-1a2b-4857-8b73-c0958885739d"  # v3

	def __init__(self, input_file, output_file = "out.csv"):
		self.input_file = input_file
		self.output_file = output_file

	def recognize_form(self):
		# [START recognize_custom_forms]
		from azure.core.credentials import AzureKeyCredential
		from azure.ai.formrecognizer import FormRecognizerClient


		form_recognizer_client = FormRecognizerClient(
			endpoint=self.endpoint, credential=AzureKeyCredential(self.api_key)
		)

		# Make sure your form's type is included in the list of form types the custom model can recognize
		with open(self.input_file, "rb") as f:
			poller = form_recognizer_client.begin_recognize_custom_forms(
				model_id = self.model_id, form=f
			)
		
		self._form = poller.result()[0]

	
	def form_to_dict(self):

		if not hasattr(self, "_form"):
			self.recognize_form()

		# -----------------------------------------------------------------
		# extracting form data
		form_dict = {}
		
		def correct_name(name):
			name_corrections = {
				"HMIS Consent Signed": "HMIS Consent signed - Yes",
				"HMIS Consent Signed - No": "HMIS Consent signed - No",
				"Ethnicity - Hipanic/Latino": "Ethnicity - Hispanic/Latino"
			}
			if name in name_corrections:
				return name_corrections[name]
			else:
				return name
		
		for name, field in self._form.fields.items():
			form_dict[correct_name(name)] = {
				"Value" : field.value,
				"Confidence":  field.confidence
			}
		    	
		# -----------------------------------------------------------------
		# grouping and cleaning form data
		cleaned_dict = {}    
		
		# getting singular attributes
		for datapoint in pair_data.PAIRS:
			key = datapoint.key()
			if key in form_dict:
				cleaned_dict[key] = form_dict[key]
				del form_dict[key]

		# getting attributes with multiple labels
		for datapoint in pair_data.PAIRS:
			key = datapoint.key()
			if key not in cleaned_dict:
				cleaned_dict[key] = {}
				for val_type in datapoint.value_types():
					fullkey_name = key + " - " + val_type
					cleaned_dict[key][val_type] = form_dict[fullkey_name]
					del form_dict[fullkey_name]
		
		self.form_dict = cleaned_dict
		return cleaned_dict

	def extract_pairs(self):
		
		# extracting form data
		if not hasattr(self, "form_dict"):
			self.form_dict = self.form_to_dict()

		pairs = {}

		# extracting Assessment Type and Level
		pairs["Assessment Type"] = self.form_dict["Assessment Type"]["Value"]
		pairs["Assessment Level"] = self.form_dict["Assessment Level"]["Value"]
		
		# extracting pronouns
		pronouns_extracted = self.form_dict["Pronouns"]["Value"].lower()
		for s in ["she", "her", "hers"]:
			if s in pronouns_extracted:
				pairs["Pronouns"] = "she/her/hers"
		if "Pronouns" not in pairs:
			for s in ["they", "them", "theirs"]:
				if s in pronouns_extracted:
					pairs["Pronouns"] = "they/them/theirs"
		if "Pronouns" not in pairs:
			for s in ["he", "him", "his"]:
				if s in pronouns_extracted:
					pairs["Pronouns"] = "he/him/his"

		for datapoint in pair_data.PAIRS:
			key = datapoint.key()
			if key not in pairs:
				# strings, integers, dates
				if datapoint.data_type() not in [pair_data.Types.CHOICE, pair_data.Types.BOOLEAN]:
					pairs[key] = self.form_dict[key]["Value"]
					if type(self.form_dict[key]["Value"]) is str:
						pairs[key] = pairs[key].title()
				# extracting non-choice values
				else:
					# multiple-choice questions and booleans
					
					# if finding primary language, check "Other" field first
					if key == "Primary Language" and self.form_dict[key]["Other"]["Value"] is not None:
						pairs[key] = self.form_dict[key]["Other"]["Value"].title()
						continue
					
					value_types = datapoint.value_types()
					# find selected value (if any)
					for value_type in value_types:
						if self.form_dict[key][value_type]["Value"] == 'selected':
							pairs[key] = value_type

					# infer selected value (if all but one unselected and one undetected)
					if key not in pairs:
						undetected_value_types = [v for v in value_types if self.form_dict[key][v]['Value'] is None]
						if len(undetected_value_types) == 1:
							pairs[key] = undetected_value_types[0]
				
				# value could not be detected or ascertained
				if key not in pairs:
					pairs[key] = None

		self.pairs = pairs  # store pairs
		# return pairs
		return pairs
			
			
	def write_to_csv(self):
		# extracting form data
		if not hasattr(self, "pairs"):
			self.extract_pairs()

		keys = [datapoint.key() for datapoint in pair_data.PAIRS]
		values = [self.pairs[key] for key in keys]
		for val, idx in enumerate(values):
			if val is None:
				values[idx] = ""
		
		# write to csv file named output_file
		with open(self.output_file, "w", newline = "") as outfile:
			writer = csv.writer(outfile, delimiter=',')
			writer.writerow(keys)
			writer.writerow(values)
			
