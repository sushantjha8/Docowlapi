import gradio as gr
from PIL import Image

from DocOwl.docowl_infer import DocOwlInfer


model_path='./chatmodel'
docowl=DocOwlInfer(ckpt_path=model_path, anchors='grid_9', add_global_img=True)
print('load model from ', model_path)

# # VQA with detailed explanation
# image='./DocDownstream-1.0/imgs/DUE_Benchmark/DocVQA/pngs/rnbx0223_193.png'
# query='What is the Compound Annual Growth Rate (CAGR) for total assets? Answer the question with detailed explanation.'



def process_inputs(image, text):
    # For demonstration, we simply return the inputs
    answer=docowl.inference(image, text)
    print(answer)

    return image, answer

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Image and Text Upload Dashboard NER")
    big_block = gr.HTML("""
    <div class ="main"style='height: 800px; width: 100px; background-color: pink;'>
                  <! -----------------------------code here    ------------!>   
                        
                        
                        
                        
                        
                        
                        </div>
    """)

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload an Image")
            text_input = gr.Textbox(label="Enter some text")

        with gr.Column():
            image_output = gr.Image(label="Uploaded Image")
            text_output = gr.Textbox(label="Entered Text")

    submit_button = gr.Button("Submit")

    # Define the interaction between inputs and outputs
    submit_button.click(
        fn=process_inputs,
        inputs=[image_input, text_input],
        outputs=[image_output, text_output]
    )

# Launch the Gradio app
demo.launch(share=True)
