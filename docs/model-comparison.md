# Model Comparison — Image 1 (Trans Pride Mural)

A human-in-the-loop spot-check comparing four vision-language models on the first image from the LoCoMo visual ground truth dataset.

**Image:** `i.redd.it/l7hozpetnhlb1.jpg` — A street mural featuring a cartoon character with pink hair, headphones, and a "TRANS PRIDE" sign.

**Models tested:**

| Model | Params | Quant | Source |
|---|---|---|---|
| LLaVA 7B | 7B | — | Flight recorder extraction |
| Moondream 2 | 1.8B | — | Ollama cache |
| MiniCPM-V | 2B | — | Ollama cache |
| Qwen2.5VL | 3B | Q4_K_M | Ollama cache |

## Human Ground Truth

A mural / street art piece. It has minor black graffiti defacement with peeling stickers near it.

The centerpiece is a cartoon character with short pink hair, large headphones, holding a trans pride flag on a handle reading **"TRANS PRIDE"**.

Additional mural details:
- Giant rainbow lettering visible (final letter is an **"e"**)
- A heart with **X's for eyes** and a smile, with crossbones underneath
- **Butterflies** painted into the mural
- **"You're Beautiful"** graffiti painted over the rainbow lettering

Surrounding environment:
- Sidewalk in the foreground
- **ADSTON** signs above the mural
- A **security camera** in the top right corner
- Below the camera: **"CAUTION SITE ENTRANCE 25m AHEAD"**
- Lights hanging above a crosswalk
- Scaffolding behind the mural covered by tarps labeled **"SAFEGORD CLASSIC FR"**
- A partially obstructed entrance area with a sign reading **"ANA COFFEE CO."** (preceding letters obscured: BANA/MANA/ZANA/unknown)
- An orange pole with various stickers and advertisements attached

## Comparison Table

| Detail | LLaVA 7B | Moondream 2 | MiniCPM-V | Qwen2.5VL |
|---|---|---|---|---|
| Trans character, pink hair, headphones | ❌ mislabels as "sticker" | ✅ | ✅ | ✅ |
| "TRANS PRIDE" sign | ✅ | ✅ | ✅ | ✅ |
| ADSTON signs | ❌ | ❌ invents "Adston Trans Centre" | ✅ | ✅ |
| "CAUTION SITE ENTRANCE 25m AHEAD" | ❌ | ❌ | ✅ | ✅ |
| "SAFEGORD CLASSIC FR" | ❌ | ❌ | ✅ | ❌ |
| "ANA COFFEE CO." | ❌ | ❌ | ✅ | ❌ |
| "You're Beautiful" graffiti | ❌ | ❌ | ✅ | ❌ |
| Tarp / scaffolding | ❌ | ❌ | ❌ | ✅ |
| Security camera (top right) | ❌ | ❌ | ❌ | ❌ |
| Butterflies | ❌ | ❌ | ❌ | ❌ |
| Heart with X eyes + crossbones | ❌ | ❌ | ❌ | ❌ |
| Rainbow lettering ending in "e" | ❌ | ❌ | ❌ | ❌ |
| Orange pole with stickers | ❌ | ❌ | ❌ | ❌ |
| Peeling stickers / black graffiti | ❌ | ❌ | ❌ | ❌ |
| **Hallucinations** | street signs, traffic lights | "rainbow", "bird", "tree", "Trans Centre" | — | — |

## Verdict

**MiniCPM-V (2B) wins.** It captured the hardest OCR targets — `SAFEGORD CLASSIC FR`, `ANA COFFEE CO.`, and `You're Beautiful` — that every other model missed. Zero hallucinations. Only 2 billion parameters.

**Qwen2.5VL (3B) is a strong second.** Zero hallucinations. Correctly identified the tarp/scaffolding that MiniCPM missed. Missed some fine-print signs and the graffiti text.

**Moondream 2 (1.8B)** hallucinated non-existent elements (rainbow, bird, tree, a fictional "Adston Trans Centre" sign).

**LLaVA 7B** mischaracterized the entire mural as "stickers" and invented street signs and traffic lights that aren't there.

### What all models missed

None of the four models detected the butterflies, the heart-with-crossbones, the rainbow lettering, the security camera, or the orange pole with stickers. These are small decorative iconographic elements that current small-scale VLMs appear blind to — their strengths are OCR and broad scene description, not fine-grained symbol detection.
