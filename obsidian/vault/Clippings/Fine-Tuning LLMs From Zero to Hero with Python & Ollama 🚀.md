---
title: "Fine-Tuning LLMs: From Zero to Hero with Python & Ollama 🚀"
source: "https://pub.towardsai.net/fine-tuning-llms-from-zero-to-hero-with-python-ollama-52258966bb6d"
author:
  - "[[MahendraMedapati]]"
published: 2025-08-19
created: 2026-05-16
description: "Fine-Tuning LLMs: From Zero to Hero with Python & Ollama 🚀 Ever wondered how to make AI models actually useful for YOUR specific needs? Let me show you how I went from confused beginner to …"
tags:
  - "clippings"
---
## Ever wondered how to make AI models actually useful for YOUR specific needs? Let me show you how I went from confused beginner to fine-tuning wizard in just one weekend!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V5uXMu312dSutd8aIGt1iQ.png)

## 📰 For Non-Members:

You can read this article without a Medium/TowardsAI membership here: [Fine-Tuning LLMs: From Zero to Hero with Python & Ollama](https://pub.towardsai.net/fine-tuning-llms-from-zero-to-hero-with-python-ollama-52258966bb6d?sk=db1305ee62ae1a1dce08d18ef288a00f)

## The “Aha!” Moment That Changed Everything 💡

Picture this: You’re trying to get ChatGPT to extract product information from messy HTML, but it keeps giving you different formats every time. Sometimes it’s a paragraph, sometimes bullet points, sometimes it just… forgets half the data. Sound familiar?

That was me three months ago, until I discovered the magic of **fine-tuning**. And trust me, once you get this right, you’ll never go back to begging AI models to “please be consistent” in your prompts.

## What Exactly IS Fine-Tuning? (The Chef Analogy) 👨🍳

Think of it like this: You hire Gordon Ramsay (he’s amazing at cooking everything), but you need him to master your grandma’s secret pasta recipe. Instead of teaching him to cook from scratch, you just show him 100 examples of the perfect dish.

That’s fine-tuning!

- **Base model** = Gordon Ramsay’s general cooking skills
- **Your training data** = Grandma’s recipe examples
- **Fine-tuned model** = Gordon now makes perfect pasta every single time

## When Should You Actually Fine-Tune? 🤔

Don’t fine-tune everything! It’s like buying a Ferrari for grocery runs. Here’s when it makes sense:

- **Strict formatting needed** — JSON outputs, legal documents, structured data
- **Domain-specific jargon** — Medical reports, legal docs, company-specific terminology
- **Cost optimization** — Use smaller, specialized models instead of expensive GPT-4 calls
- **Privacy concerns** — Keep sensitive data on your own servers

## Quick Reality Check: Alternatives First! ⚡

Before diving into fine-tuning, try these:

- **Prompt engineering** (free, but inconsistent)
- **RAG (Retrieval-Augmented Generation)** (add context on-the-fly)
- **Few-shot prompting** (give examples in your prompt)

If these don’t cut it, then fine-tuning is your answer!

## The Complete Step-by-Step Guide 📋

Alright, let’s get our hands dirty! We’re using:

- **Unsloth** (makes fine-tuning 2x faster and free!)
- **Google Colab** (free GPU — no fancy hardware needed)
- **Phi-3 Mini** (small but mighty base model)
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bkM-dp67o2CSUAJeQoTvrg.png)

## Step 1: Gather Your Golden Dataset 📊

This is make-or-break territory. Bad data = bad model, period.

You need **input-output pairs** in JSON format. Here’s what mine looked like for HTML extraction:

```c
[
  {
    "input": "<div><h2>Product: Gaming Laptop</h2><p>Price: $1299</p><span>Category: Electronics</span><span>Brand: ASUS</span></div>",
    "output": {"name": "Gaming Laptop", "price": "$1299", "category": "Electronics", "brand": "ASUS"}
  },
  {
    "input": "<div><h2>Product: Coffee Mug</h2><p>Price: $15</p><span>Category: Kitchen</span><span>Brand: Starbucks</span></div>",
    "output": {"name": "Coffee Mug", "price": "$15", "category": "Kitchen", "brand": "Starbucks"}
  }
]
```

**Pro tip:** Start with just 20–30 examples for quick testing, then scale to 100–500 for production quality!

## Step 2: Set Up Your Free GPU Powerhouse ⚡

Head to [Google Colab](https://colab.research.google.com/) and follow these steps:

1. **Create new notebook**
2. **Runtime → Change runtime type → T4 GPU** (If T4 isn’t available, choose V100 or P100)
3. **Upload your JSON dataset**

Install the magic ingredients:

```c
# This takes about 2 minutes - grab a coffee! ☕
!pip install unsloth
# Alternative for latest features (if needed):
# !pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps trl peft accelerate bitsandbytes transformers datasets
```

Verify your GPU setup:

```c
import torch
print(f"GPU Available: {torch.cuda.is_available()}")  
print(f"GPU Name: {torch.cuda.get_device_name(0)}")
# Should show: Tesla T4 or similar
```

## Step 3: Load Your Base Model 🤖

Time to wake up our AI assistant:

```c
from unsloth import FastLanguageModel

model_name = "unsloth/phi-3-mini-4k-instruct-bnb-4bit"
max_seq_length = 2048  # Adjust based on your data length
dtype = None  # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True  # Use 4bit quantization to reduce memory usage
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)
```

This downloads the model (5–10 minutes). Perfect time for a snack break! 🍪

## Step 4: Transform Your Data into AI Food 🍽️

```c
import json
from datasets import Dataset

# Load your dataset
with open("your_dataset.json", "r") as f:
    data = json.load(f)
# Format for training - using chat template
def format_chat_template(item):
    return tokenizer.apply_chat_template(
        [
            {"role": "user", "content": item['input']},
            {"role": "assistant", "content": json.dumps(item['output'])}
        ],
        tokenize=False,
        add_generation_prompt=False
    )
# Create the training dataset
formatted_data = [{"text": format_chat_template(item)} for item in data]
dataset = Dataset.from_list(formatted_data)
# Check what it looks like
print("Sample training example:")
print(formatted_data[0]["text"])
```

## Step 5: Add LoRA Magic ✨

**LoRA** (Low-Rank Adaptation) is the secret sauce that makes fine-tuning efficient. Instead of retraining the entire model, we add small “adapter” layers:

```c
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # Rank - higher = more parameters
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", 
                   "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407
)
```

You’ll see: `"Unsloth: Patched 32 layers with LoRA..."` - that's success! 🎉

## Step 6: Train Your Custom AI 🏋️♂️

Here’s where the magic happens:

```c
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,  # Increase for more training
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        optim="adamw_8bit",  # Use "adamw_torch" if you get optimizer errors
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
        save_steps=30,
    ),
)
# Start training! 🚀
trainer.train()
```

Watch that loss go down! Lower = better. Takes about 10–15 minutes for 500 examples.

## Step 7: Test Your Creation 🧪

Let’s see if it actually works:

```c
# Switch to inference mode
FastLanguageModel.for_inference(model)

# Test input
test_html = "<div><h2>Product: Wireless Headphones</h2><p>Price: $79</p><span>Category: Audio</span><span>Brand: Sony</span></div>"
# Format input using chat template
messages = [{"role": "user", "content": test_html}]
inputs = tokenizer.apply_chat_template(
    messages, 
    tokenize=True, 
    add_generation_prompt=True, 
    return_tensors="pt"
).to("cuda")
# Generate response
with torch.no_grad():
    outputs = model.generate(
        input_ids=inputs, 
        max_new_tokens=256, 
        use_cache=True,
        temperature=0.1,  # Low temp = more consistent
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
# Extract just the new generated text (not the full conversation)
response = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
print("Model output:")
print(response.strip())
```

**Expected output:**

```c
{"name": "Wireless Headphones", "price": "$79", "category": "Audio", "brand": "Sony"}
```

If it’s inconsistent, train for more steps!

## Step 8: Export for Ollama (Run Locally!) 💻

This is where it gets exciting — run your model locally, privately:

```c
# Export to GGUF format (Ollama-compatible) - This is Unsloth-specific!
model.save_pretrained_gguf(
    "fine_tuned_model", 
    tokenizer, 
    quantization_method="q4_k_m"  # Good balance of size/quality
)
```

**Important:** This `save_pretrained_gguf` function is specific to Unsloth - it won't work with regular Hugging Face models!

Download the files from Colab (right-click → Download). This takes 10–20 minutes.

## Step 9: Set Up Ollama (Your Local AI Server) 🏠

1. **Install Ollama:** Visit [ollama.com](https://ollama.com/) and download for your OS
2. **Create your model directory:**
```c
cd ~/Downloads
mkdir my-fine-tuned-model
mv unsloth.Q4_K_M.gguf my-fine-tuned-model/
cd my-fine-tuned-model
```
1. **Create a Modelfile:**
```c
touch Modelfile
nano Modelfile  # Or use any text editor
```

**Modelfile content:**

```c
FROM ./unsloth.Q4_K_M.gguf
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER stop ["<|endoftext|>"]
TEMPLATE "{{ .Prompt }}"
SYSTEM "You are a specialized HTML data extraction assistant."
```
1. **Create your Ollama model:**
```c
ollama create html-extractor -f Modelfile
```

## Step 10: Enjoy Your Custom AI! 🎉

```c
ollama run html-extractor
```

Now paste any HTML and watch your model extract **perfect, consistent JSON every single time** — that’s the real magic of fine-tuning!

## Pro Tips That’ll Save You Hours ⚡

- **Start small:** 100 examples → test → add more if needed
- **Diverse data:** Don’t just use similar examples — variety prevents overfitting
- **Save checkpoints:** Add `save_steps=30` to avoid losing progress
- **Monitor loss:** Should decrease steadily - if it doesn't, check your data
- **Temperature matters:** Use 0.1-0.3 for consistent outputs, 0.7+ for creativity

## Common Pitfalls (Learn from My Mistakes!) 😅

- **Inconsistent formatting** → More training steps or better data
- **“Hallucinations”** → Need more diverse examples
- **Out of memory errors** → Reduce batch size or sequence length
- **Slow training** → Use Unsloth (2x speedup) and enable bf16
- **Model not loading in Ollama** → Check GGUF file isn’t corrupted

## What’s Next? 🚀

Now that you’ve mastered the basics, here are some exciting directions:

- **Try larger models:** Llama 3.1 8B for even better results
- **Multi-task training:** One model for multiple extraction tasks
- **Advanced techniques:** QLoRA, gradient checkpointing, custom loss functions
- **Deployment:** Docker containers, API endpoints, web interfaces

## Final Thoughts 💭

Fine-tuning felt intimidating at first, but breaking it down step-by-step made it totally manageable. The best part? Once you have this workflow down, you can fine-tune models for ANY task in under an hour.

Whether you’re extracting data, generating specific formats, or creating domain experts, fine-tuning gives you superpowers that no amount of prompt engineering can match.

**What will you fine-tune first?** Drop a comment below — I’d love to hear about your projects!

And if this guide helped you, give it a clap 👏 and follow for more hands-on AI tutorials!

## 🚀 Want to Master More AI?

**Subscribe to my** [**YouTube channel**](https://www.youtube.com/@tech_with_mahendra) for in-depth tutorials, hands-on coding sessions, and the latest AI insights! 📺✨

👆 *Hit that subscribe button and ring the notification bell to never miss cutting-edge content!*

## 🔗 Let’s Connect & Collaborate!

I’m passionate about sharing knowledge and building amazing AI solutions. Let’s connect:

🐙 **GitHub:** [**Link**](https://github.com/MahendraMedapati27) — Check out my latest projects and code repositories

💼 **LinkedIn:** [**Link**](https://www.linkedin.com/in/mahendra-medapati-429239289) — Connect for professional discussions and industry insights

📧 **Email:** [\[Mahendra Medapati\]](http://mahendramedapati.r469@gmail.com/) — Reach out directly for inquiries or collaboration

🐦 **X:** [Link](https://x.com/MahendraM27) — Follow for updates, thoughts, and discussions on AI

☕ **Support me:** [Buy Me a Coffee Link](https://buymeacoffee.com/mahendramedapati) — Help me create more content

**Tags:** #MachineLearning #AI #Python #LLM #FineTuning #Ollama #DeepLearning #DataScience