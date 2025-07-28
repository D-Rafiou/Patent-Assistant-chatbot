import os
import pdfplumber
import json
import nltk # library that we are using to make sure that each chunk does not cut off mid sentence
nltk.download('punkt_tab')

max_words = 300 # this is 450 - 600 tokens which will work well for using rage with Gronk
overlap = 50

data = "./data/mpep"
output_file = "./output/output.jsonl"

def clean_text(text):
    return ' '.join(text.split()) # remove excessive spacing

#method to parse each html file and return a text
def parse_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return clean_text(text.strip())


def chunk_pdf(text, max_words=max_words, overlap=overlap):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for i, sentence in enumerate(sentences):
        sentence_words = sentence.split()
        sentence_length = len(sentence_words)
        
        # Check if adding this sentence would exceed max chunk size
        if current_length + sentence_length > max_words:
            chunks.append(' '.join(current_chunk))
            # Start new chunk with overlap sentences if possible
            if overlap > 0:
                # Overlap: keep last `overlap` words from current chunk
                overlap_words = ' '.join(current_chunk).split()[-overlap:]
                current_chunk = overlap_words.copy()
                current_length = len(current_chunk)
            else:
                current_chunk = []
                current_length = 0
        
        current_chunk.extend(sentence_words)
        current_length += sentence_length
    
    # Add last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks



def main():
    with open(output_file,"w", encoding="utf-8") as out_f:
        for(dirname,dirpath,filenames) in os.walk(data):
            for filename in filenames:
                file = os.path.join(data,filename)
                section = filename.replace(".pdf","")
                section_num,*section_title= section.split("_")
                text = parse_pdf(file)
                chunks = chunk_pdf(text)
                for i,chunk in enumerate(chunks):
                    json.dump({
                        "text": chunk,
                        "section_title": ' '.join(section_title),
                        "section_number":section_num,
                        "chunk_index" : i
                        
                    },out_f)
                    out_f.write("\\n")
    print(f"Successfully saved chunks to {output_file}")



    
main()