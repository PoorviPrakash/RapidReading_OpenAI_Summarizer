from flask import Flask, render_template, request, jsonify
import openai
import openpyxl 
import re


app = Flask(__name__)
openai.api_key = ''

#function to divide the paper into chunks 
def divide_into_chunks(input_string, chunk_size):
    chunks = []
    #Diving the input text depending on the chunk size specified
    for i in range(0, len(input_string), chunk_size):
        chunk = input_string[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

#getting the summary of each chunk using ChatGPT
def getSummariesGPT(chunks):
  out_token = 3300
  summaries=[]
  for txt in chunks:
    #Calling the openAI API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=txt + "Summarize the above passage including important result data. The output should be a passage and lesser than the size of the input.",
        max_tokens = out_token,
        temperature = 0.0,
    )
    # pass the generated summary
    res = response["choices"][0]["text"]
    summaries.append(res)
  return summaries

#Make ChatGPT api call to extract the key info from the combined summary
def getResults(combinedTxt): 
  print(combinedTxt)
  out_token = 3000
  #Asking the query prompt
  prompt_txt = combinedTxt + "Answer the following questions from the above passage - 1. Research Paper Name, 2. conclusion  , 3. no. of subjects , 4. relative risk , 5. length of follow , 6. Outcome Measures , 7. Statistical Analysis , 8. Limitations , 9. Funding , 10. Conflicts of Interest. Maintain seriel Number."
  print(prompt_txt)
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt= prompt_txt,
    max_tokens = out_token,
    temperature = 0.0,
  )
  result_data = response["choices"][0]["text"]
  return result_data

#Spliting the result data by the seriel numbers
def split_text_by_serial_numbers(text):
    pattern = r'\d\.'
    split_list = re.split(pattern, text)
    split_list = [item.strip() for item in split_list if item.strip()]
    return split_list


#Setting the first route to process the input text and do the processing to get data from ChatGPT
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the data from request body
        data = request.get_json()
        input_data = data['input_data']

        chunk_size = 1200
        allChunks = divide_into_chunks(input_data, chunk_size)
        allSummaries = getSummariesGPT(allChunks)
        combined_summary = ''.join(allSummaries)
        #Run while loop wntil the combined summary is less than 4000 tokens
        while len(combined_summary)>4000:
            allChunks = divide_into_chunks(combined_summary, chunk_size)
            allSummaries = getSummariesGPT(allChunks)
            combined_summary = ''.join(allSummaries)

        result = getResults(combined_summary)

        # Send the obtained data
        response_data = {
            'result': result
        }
        return jsonify(response_data)

    return render_template('index.html')

#Setting the route to pass the result data into the excel sheet
@app.route('/excel', methods=['POST'])
def excelDataLoad():
    # Get the data from request body
    data = request.get_json()
    print(data)
    list_data = data['list_data']
    
    # Set file path
    file_path = ""

    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)

    # Select the desired worksheet
    sheet = workbook.active

    sdata = split_text_by_serial_numbers(list_data)
    row = tuple(sdata)

    # append data to excel
    sheet.append(row)

    # Save the modified Excel file
    workbook.save(file_path)

    # Save the processed data to Excel and send status
    response_data = {
        'status': "file updated"
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
