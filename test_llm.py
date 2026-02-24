
from backend import HiringAssistantBackend
try:
    bot = HiringAssistantBackend(use_openai_fallback=False, session_id='test1234')
    # Suppress warnings
    import warnings
    warnings.filterwarnings('ignore')
    out1 = bot.process_message('Hi, my name is Alice.')
    print('OUTPUT 1:', out1)
    print('History length:', len(bot.chat_history.messages))
except Exception as e:
    print('FAIL:', e)

