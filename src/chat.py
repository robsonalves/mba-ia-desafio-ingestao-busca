from search import search_and_answer


def main():
    print("=" * 50)
    print("Chat RAG - Pergunte sobre o documento")
    print("Digite 'sair' para encerrar")
    print("=" * 50)

    while True:
        try:
            pergunta = input("\nFaça sua pergunta: ").strip()

            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Encerrando...")
                break

            if not pergunta:
                continue

            print("\nProcessando...")
            resposta = search_and_answer(pergunta)
            print(f"\nRESPOSTA: {resposta}")

        except KeyboardInterrupt:
            print("\n\nEncerrando...")
            break


if __name__ == "__main__":
    main()
