from DocOwl.docowl_infer import DocOwlInfer

model_path = "./chatmodel"
docowl = DocOwlInfer(ckpt_path=model_path, anchors="grid_9", add_global_img=True)
print("load model from ", model_path)

# VQA with concise phrases
image = "./DocDownstream-1.0/imgs/DUE_Benchmark/DocVQA/pngs/rnbx0223_193.png"
query = "What is the Compound Annual Growth Rate (CAGR) for total assets?"
answer = docowl.inference(image, query)
print(answer)

# VQA with detailed explanation
image = "./DocDownstream-1.0/imgs/DUE_Benchmark/DocVQA/pngs/rnbx0223_193.png"
query = "What is the Compound Annual Growth Rate (CAGR) for total assets? Answer the question with detailed explanation."
answer = docowl.inference(image, query)
print(answer)
