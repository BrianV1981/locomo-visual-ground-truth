# LoCoMo Visual Ground Truth & OCR Cache

<div align="center">
  <a href="https://www.buymeacoffee.com/BrianV1981" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
  <p><em>Nobody is paying me to fix this broken dataset. If this repository saved you days of compute time, API tokens, or academic headaches, please consider supporting my work so I can continue repairing open-source AI infrastructure!</em></p>
</div>

---

The definitive visual ground truth dataset and multi-model Optical Character Recognition (OCR) translation cache for the [LoCoMo (Long-term Conversational Memory)](https://github.com/snap-research/locomo) Benchmark.

## 🚨 The Link Rot Crisis

The original LoCoMo benchmark evaluates Multimodal AI Agents by requiring them to read and remember facts from images shared in long-term chat histories. 

However, because the dataset relied on live internet URLs (Reddit, Flickr, personal blogs) instead of hosting the images, the benchmark has succumbed to severe **Link Rot**. 
Our forensic triage discovered that exactly **10% of the dataset's unique images (87 out of 862) are now permanently dead (HTTP 404/402)**. 

Because the original dataset's fallback mechanism (`blip_caption`) is blind to text (e.g., describing a book titled "Nothing is Impossible" merely as "a book with a coin"), **82 questions in the benchmark are now mathematically impossible to answer**.

## 🛠️ What This Repository Provides

To permanently fix this for the AI research community, we have built the ultimate visual safety net.

### 1. The Image Preservation Archive
We have downloaded, sanitized, and preserved the remaining **775 alive images**. 
To strictly adhere to **Fair Use (17 U.S.C. § 107)** for non-commercial academic research, all images have been aggressively downscaled to a maximum dimension of 1920x1080 (removing their high-resolution commercial value) and stripped of alpha channels while perfectly preserving the semantic data and OCR text needed to pass the benchmark.

### 2. The Question-to-Image Matrix
We built a precise forensic map (`question_image_matrix.csv`) linking all 1,986 LoCoMo questions to their exact visual dependencies.
* **1,251** Pure Text Questions
* **653** Verifiable Image Questions (Links are alive)
* **82** Dead Image Questions (Links are dead, questions unanswerable)

**The Unused Image Discovery:** We also discovered **377 unused alive images** in the dataset (`unused_alive_urls.json`). These are valid photos shared in the chat histories that the original annotators never wrote questions for. These are currently being used by the [LoCoMo V2](https://github.com/BrianV1981/locomo-v2) project to replace the 82 dead questions.

### 3. The Multi-Model OCR Translation Cache (WIP)
We are currently running a diverse suite of state-of-the-art Vision-Language Models over all 775 alive images to extract deep, text-rich descriptions (transcribing signs, book titles, and posters that BLIP missed). 

**The goal of this repository is to become the central hub for LoCoMo visual translations.** 
We are building a multi-model JSON cache so future researchers can simply choose which model's "lens" they want to evaluate against. Injecting these rich descriptions into your text pipelines allows you to completely bypass the broken internet links and achieve true multimodal evaluation for **$0 in API costs and zero wasted compute time**.

#### Current Model Progress
- [x] **LLaVA-7B** *(Currently processing...)*
- [ ] **Qwen2.5-VL**
- [ ] **Llama 3.2-Vision**
- [ ] **Pixtral 12B**
- [ ] **Gemini 1.5 Pro / Flash**
- [ ] **GPT-4o**
- [ ] **Claude 3.5 Sonnet**

**🤝 Call for Contributors:** Do you have API credits to spare, or a beefy local GPU? We would love your help! If you want to run the 775 images through a model not yet checked off on this list (or a brand new model), please open a Pull Request with your JSON cache. Let's build the ultimate open-source visual ground truth together!

---

## 📂 Repository Structure

- `alive_urls.json`: The exact list of 775 surviving URLs.
- `dead_urls.json`: The exact list of 87 permanently dead URLs.
- `question_image_matrix.csv`: The forensic mapping of every QA pair to its required image URL and alive/dead status.
- `unused_alive_urls.json`: 377 healthy images that have no corresponding benchmark questions.
- `locomo_pure_text.json` / `locomo_verifiable_image.json` / `locomo_dead_image.json`: The LoCoMo dataset cleanly partitioned by image dependency.
- `download_images.py`: The multithreaded Fair Use preservation script.
- `generate_matrix.py`: The forensic mapping script.

## 🔗 Related Projects
* [LoCoMo V2](https://github.com/BrianV1981/locomo-v2): The corrected, 100% solvable text and multimodal benchmark, stripped of annotator hallucinations.
