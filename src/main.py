import heapq
import re
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def summarize(text, num_sentences=3):
    text_clean = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'(?<=[.!?]) +', text_clean)
    
    if not sentences or len(sentences) <= num_sentences:
        return text

    word_frequencies = {}
    for word in text_clean.lower().split():
        word = re.sub(r'[^\w\s]', '', word)
        if word:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    sentence_scores = {}
    for sent in sentences:
        for word in sent.lower().split():
            word = re.sub(r'[^\w\s]', '', word)
            if word in word_frequencies:
                if len(sent.split()) < 30:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    # Sort sentences back to original order
    original_order_summary = [sent for sent in sentences if sent in summary_sentences]

    return ' '.join(original_order_summary)

def run_summarization(text):
    if not text.strip():
        console.print("[red]✖ Teks kosong.[/red]")
        return
        
    num_sentences = Prompt.ask("Berapa kalimat ringkasan yang diinginkan?", default="3")
    try:
        num_sentences = int(num_sentences)
    except ValueError:
        num_sentences = 3
        
    console.print("\n[bold green]Memproses...[/bold green]\n")
    summary = summarize(text, num_sentences)
    
    console.print(Panel(Text(summary, justify="left"), title="[bold cyan]Ringkasan[/bold cyan]", border_style="cyan"))

def main():
    console.clear()
    console.print(Panel.fit("[bold blue]Noceur NLP Toolkit[/bold blue]\n[dim]Extractive Text Summarizer[/dim]", border_style="blue"))

    while True:
        console.print("\n[bold]Menu:[/bold]")
        console.print("  [1] Input teks langsung")
        console.print("  [2] Baca dari file (txt/md)")
        console.print("  [3] Keluar\n")

        choice = Prompt.ask("[bold cyan]Pilih menu[/bold cyan]", choices=["1", "2", "3"], default="1")

        if choice == "1":
            console.print("[cyan]Masukkan teks panjang Anda di bawah ini (tekan Enter 2 kali untuk selesai):[/cyan]")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            
            text = " ".join(lines)
            run_summarization(text)
            
        elif choice == "2":
            file_path = Prompt.ask("[cyan]Masukkan path file[/cyan]")
            file_path = file_path.strip().strip('"').strip("'")
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                console.print(f"[green]✔ Berhasil membaca '{file_path}' ({len(text)} karakter)[/green]")
                run_summarization(text)
            else:
                console.print(f"[bold red]✖ File tidak ditemukan: {file_path}[/bold red]")
                
        elif choice == "3":
            console.print("[bold magenta]Terima kasih telah menggunakan Noceur NLP Toolkit![/bold magenta] 🧠\n")
            break

if __name__ == "__main__":
    main()
