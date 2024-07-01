## VimSonnet

version 1 can do one-two web page operations like post a tweet on twitter

<blockquote class="twitter-tweet" data-media-max-width="560"><p lang="en" dir="ltr">all i wanted to do was post a tweet by claude and that has been done. the screen coordinate approach doesn&#39;t work unless your vision model supports coordinates (some can do, some getting cooked). this approach uses vimium hint tags + pyautogui + 3.5 sonnet function calls <a href="https://t.co/w32UBKBM60">https://t.co/w32UBKBM60</a> <a href="https://t.co/8tCYDMLEhT">pic.twitter.com/8tCYDMLEhT</a></p>&mdash; sankalp (@dejavucoder) <a href="https://twitter.com/dejavucoder/status/1807387424018084345?ref_src=twsrc%5Etfw">June 30, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Disclaimer: Not a robust project, experimental in nature

- This project creates an AI assistant using Claude 3.5 Sonnet to control a web browser via Vimium extension commands.
- It can take screenshots, execute Vimium commands, type text, and perform searches using hint tags or Vimium's search box.
- The assistant uses a series of function calls to interact with the browser, including screenshot capture, text input, and command execution.
- The system employs a conversational loop, allowing for multiple actions based on user input and AI responses.
- Search functionality and URL copy/paste features are included but are still in an experimental stage.

Setup:
1. Clone the repository: `git clone https://github.com/sankalp1999/vimSonnet.git`
2. Navigate to the project directory
3. Create a virtual environment: `python -m venv myenv`
4. Activate the virtual environment: `source myenv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Export your Anthropic API key: `export ANTHROPIC_API_KEY=your_api_key_here`

Remember to replace 'your_api_key_here' with your actual Anthropic API key.