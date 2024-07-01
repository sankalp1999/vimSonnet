## VimSonnet

Thanks to Ishan's project [vimGPT](https://github.com/ishan0102/vimGPT), I got to know about the Vimium extension. 

Version 1 can do one-two web page operations like [post a tweet on X](https://x.com/dejavucoder/status/1807387424018084345)

Version 2 is an attempt to make it able to search and copy/paste URLs. It's not robust yet. 



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

**This works only on Mac** To make it work on other OS, change the `focus_chrome` function accordingly.

## Possible updates

- Make search more robust
- Add vertical support for more commands
