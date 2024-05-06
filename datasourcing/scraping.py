from bs4 import BeautifulSoup

html = '''
<div style="width:375px;margin-left:10px;
    margin-right:10px; margin-top:15px;
    text-align:left;
    font-family:Verdana;font-size:1px;
    color:#0d0d0d; line-height:1.7em;float:left;">
<section>
<div id="ctl00_cntrightpanel_pnlRcpMethod">
<span class="recipe_subheader">Method</span>
<div id="recipe_small_steps">
<span style="margin:0;padding:0;display:inline;font-weight:normal;font-size:15px;line-height:1.7em;">
<span class="recipe_subheader" id="procsection1"><br/>For sabudana khichdi in microwave</span><br/><ol itemprop="recipeInstructions" itemscope itemType="https://schema.org/HowToSection" itemprop="name" class="rcpprocsteps"><span style="display:none;" itemprop="name">For sabudana khichdi in microwave</span><li id="proc1" itemprop="itemListElement" itemscope itemType="https://schema.org/HowToStep"><span itemprop="text">To make <span class="bold1">sabudana khichdi in microwave</span>, wash the sago. Drain and place them in a deep bowl, add approx. ½ cup of water and mix gently. Cover with a lid and keep aside for 8 hours.</span><meta itemprop="url" content="https://www.tarladalal.com/sabudana-khichdi-in-microwave-2749r#proc1" /></li><li id="proc2" itemprop="itemListElement" itemscope itemType="https://schema.org/HowToStep"><span itemprop="text">Combine the oil, cumin seeds and curry leaves in a microwave safe bowl and microwave on high for 1 minute.</span><meta itemprop="url" content="https://www.tarladalal.com/sabudana-khichdi-in-microwave-2749r#proc2" /></li><li id="proc3" itemprop="itemListElement" itemscope itemType="https://schema.org/HowToStep"><span itemprop="text">Add the boiled potatoes, microwave on high for half a minute.</span><meta itemprop="url" content="https://www.tarladalal.com/sabudana-khichdi-in-microwave-2749r#proc3" /></li><li id="proc4" itemprop="itemListElement" itemscope itemType="https://schema.org/HowToStep"><span itemprop="text">Add the soaked sabudana, peanuts, coriander, green chilli paste, lemon juice, sugar and salt, mix gently and microwave on high for 4 minutes, while stirring once in between.</span><meta itemprop="url" content="https://www.tarladalal.com/sabudana-khichdi-in-microwave-2749r#proc4" /></li><li id="proc5" itemprop="itemListElement" itemscope itemType="https://schema.org/HowToStep"><span itemprop="text">Serve the <span class="bold1">sabudana khichdi</span> hot with curds.</span><meta itemprop="url" content="https://www.tarladalal.com/sabudana-khichdi-in-microwave-2749r#proc5" /></li></ol></span></div>
<div id="recipe_tips"> </div>
</div>
</section>
'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the div with id="recipe_small_steps" and extract its text
recipe_small_steps_div = soup.find('div', id='recipe_small_steps')

for span in recipe_small_steps_div.find_all('span'):
    print(span.get_text())

# for s in recipe_small_steps_div.stripped_strings:
#       print(s+",")

# print(small_steps_text)

# Parse the HTML
# soup = BeautifulSoup(html, 'html.parser')
#
# # Find the div with id="recipe_small_steps"
# recipe_small_steps_div = soup.find('div', id='recipe_small_steps')
#
# # Extract text from each span tag within the recipe_small_steps_div
# small_steps_text = '\n'.join(span.get_text() for span in recipe_small_steps_div.find_all('span'))
#
# print(small_steps_text)