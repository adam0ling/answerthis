import numpy as np
import torch

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer
)

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop

# random seed
def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)

def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # No generation bigger than model size
    elif length < 0:
        length = MAX_LENGTH  # avoid infinite loop
    return length


# generation
def generate_text(seed, length, prompt_text):
    # set up
    model_path = '../output10k'
    device = 'cpu'

    # set seed
    set_seed(seed)

    # Initialize the model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.to(device)

    genLength = adjust_length_to_model(length, max_sequence_length=model.config.max_position_embeddings)

    # Encode prompt
    prompt_text = 'Question: ' + prompt_text + ' Answer: '
    encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False, return_tensors="pt")
    encoded_prompt = encoded_prompt.to(device)

    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=genLength + len(encoded_prompt[0]),
        temperature=1,
        top_k=0,
        top_p=0.9,
        repetition_penalty=1,
        do_sample=True,
        num_return_sequences=1,
    )

    # Remove the batch dimension when returning multiple sequences
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()

    generated_sequences = []

    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        print("=== GENERATED SEQUENCE {} ===".format(generated_sequence_idx + 1))
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

        # remove prompt
        text = text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]

        # Remove all text after the stop token
        text = text[: text.find('Answer:') if text.find('Answer:')>0 else None]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
        total_sequence = (
            prompt_text + text
        )

        generated_sequences.append(total_sequence)
        print(total_sequence)

    return generated_sequences
