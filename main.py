from pipeline import MedicalTranscriptPipeline
from Optional6_testQuality import run_validation_pipeline
import json
def main():

    pipeline = MedicalTranscriptPipeline()

    result=pipeline.run(transcripts="record1.json",
         verbose=True
     )
    
    return result
if __name__ == "__main__":

    main()