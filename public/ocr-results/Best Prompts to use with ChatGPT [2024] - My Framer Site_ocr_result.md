July 30, 2024 by Mert Deveci
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
Best Prompts to use with ChatGPT [2024]
30 JULY 2024
5 best ChatGPT
prompts for
everyday business
usecases
godmode
Artificial intelligence is changing the way we do things, and ChatGPT is a big part of that change.
Imagine having a super-smart assistant that can help you with just about anything, from doing your
homework to writing a story.
Yet often we run into a big problem: the blank page.
Once you see an empty chatbox or a page, it can become intimidating to write a prompt and iterate on
it just to be able to get the result that you want.
So we listed down some best use cases and prompt examples for you to use.
1. Write an email selling an accounting software to local businesses
Changelog
Blog How-to Guides Community
▸
Sign in
Book a demo
information:
<business_type>
{{BUSINESS_TYPE}}
</business_type>
<software_name>
{{SOFTWARE_NAME}}
</software_name>
<key_features>
{{KEY_FEATURES}}
</key_features>
When writing the email, follow these guidelines:
1. Use a casual and friendly tone, as if you're writing to a colleague or
acquaintance.
2. Keep the language simple, clear, and concise.
3. Avoid using jargon or overly technical terms.
4. Write in a conversational style, using contractions and informal phrases
where appropriate.
Changelog
Blog
How-to Guides
Community
▸
Sign in
Book a demo
1. Start with a friendly greeting.
2. Briefly introduce yourself and the software.
3. Mention how the software can benefit the specific type of business you're
addressing.
4. Highlight 2-3 key features of the software that are most relevant to the
business type.
5. Include a call to action, such as offering a demo or free trial.
6. Close with a friendly sign-off.
Personalize the email by:
- Addressing common pain points for the specific business type
- Using examples or scenarios that relate to their industry
When mentioning the key features:
- Focus on how they solve problems or improve efficiency for the business
- Use bullet points to make the information easy to scan
- Keep descriptions brief and benefit-focused
Close the email with:
- A friendly, low-pressure invitation to learn more
Changelog Blog How-to Guides Community
▸ Sign in
Book a demo
Remember to maintain a casual, human-sounding tone throughout the email.
Imagine you're explaining the software to a friend who owns a small business.
Write your email inside <email> tags.
2. Write a Linkedin post for a salesperson working in finance
You are tasked with writing a casual, natural-sounding LinkedIn post for a
salesperson working in finance. The post should be suitable for regular
sharing on their LinkedIn profile. Here are the details you'll need to
incorporate:
<salesperson_name>
{{SALESPERSON_NAME}}
</salesperson_name>
<company_name>
{{COMPANY_NAME}}
</company_name>
<finance_area>
{{FINANCE AREA}}
</finance_area>
Guidelines for writing the post:
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
2. Avoid using any emojis or excessive punctuation.
3. The post should be brief, ideally between 2-4 sentences.
4. Include a mention of the salesperson's work in finance, specifically in
FINANCE AREA.
5. Incorporate a recent experience, insight, or thought related to their work or
industry.
6. If appropriate, add a subtle call-to-action or invitation for engagement (e.g.,
asking for opinions or experiences).
7. Use the first-person perspective, as if SALESPERSON_NAME is writing the
post themselves.
8. Mention COMPANY_NAME naturally within the context of the post.
Remember to make the post sound natural and human. Avoid overly formal
language or industry jargon unless it's commonly used in casual conversation.
Write your LinkedIn post inside <linkedin_post> tags. Do not include any
introductory text or explanations outside of these tags.
3. Summarise a document a very concise way
You are tasked with summarizing a document in a concise way for a specific
use case. Follow these instructions carefully to produce an effective summary.
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
<document>
{{DOCUMENT}}
</document>
The summary you create should be tailored for the following use case:
<use_case>
{{USE_CASE}}
</use_case>
To create an effective summary:
1. Carefully read and analyze the entire document.
2. Identify the main ideas, key points, and essential information that are most
relevant to the specified use case.
3. Prioritize information based on its importance to the use case.
4. Condense the information into a concise summary, focusing on clarity and
relevance.
5. Ensure that the summary captures the essence of the document while
addressing the needs of the use case.
6. Use clear and straightforward language, avoiding jargon unless it's essential
for the use case.
Changelog Blog How-to Guides
Community
▸
Sign in
Book a demo
Present your summary in the following format:
<summary>
[Your concise summary tailored to the use case goes here]
</summary>
<key_points>
1. [First key point relevant to the use case]
2. [Second key point relevant to the use case]
3. [Third key point relevant to the use case]
(Add more points if necessary, but aim for no more than 5)
</key_points>
Remember, the goal is to provide a summary that is both concise and highly
relevant to the specified use case. Avoid including extraneous information that
doesn't directly serve the use case's needs.
4. Reading and categorising invoices
You are an Al assistant tasked with categorizing invoices based on their
content. You will be provided with invoice data and a list of categories. Your
job is to assign each invoice to the most appropriate category.
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
<categories>
{{CATEGORIES}}
</categories>
Now, I will provide you with the invoice data:
<invoice_data>
{{INVOICE_DATA}}
</invoice_data>
Your task is to analyze each invoice in the provided data and categorize it
according to the list of categories given. Follow these steps for each invoice:
1. Carefully read the invoice details, paying attention to the items or services
listed, the company name, and any other relevant information.
2. Compare the invoice content with the provided categories.
3. Determine the most appropriate category for the invoice based on its
primary purpose or the majority of items/services listed.
4. If an invoice could potentially fit into multiple categories, choose the one
that best represents the overall nature of the purchase.
5. If you're unsure about a categorization, explain your reasoning and provide
your best guess.
decision.
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
After your reasoning, provide the categorization for each invoice in the
following format:
<categorization>
Invoice [Number]: [Chosen Category]
</categorization>
If you encounter an invoice that doesn't clearly fit into any of the provided
categories, categorize it as "Miscellaneous" and explain why in your reasoning.
Remember to be consistent in your categorization approach across all
invoices. If you notice any patterns or similarities between invoices, you may
reference your previous decisions to maintain consistency.
Begin your analysis with the first invoice and continue until you have
categorized all invoices in the provided data.
5. Find alternative products to a given product
You are tasked with finding alternative products to a given product. Your goal
is to suggest products that serve similar purposes or solve similar problems,
but may have different features, price points, or target audiences.
Here is the product for which you need to find alternatives:
Changelog Blog
How-to Guides Community
▸
Sign in
Book a demo
{{PRODUCT}}
</product>
Here is a description of the product:
<product_description>
{{PRODUCT_DESCRIPTION}}
</product_description>
First, analyze the key features and use cases of the given product. Consider
its primary function, target audience, price range, and any unique selling
points mentioned in the description.
Next, brainstorm alternative products that could serve similar purposes or
solve similar problems. These alternatives may:
- Have similar core functionality but different additional features
- Target a different price point (both higher and lower)
- Cater to a slightly different audience
- Use different technology or methods to achieve similar results
- Be from competing brands or lesser-known manufacturers
Provide a list of at least 3 and no more than 5 alternative products. For each
alternative, include:
Changelog Blog How-to Guides
Community
▸
Sign in
Book a demo
2. A brief description (1-2 sentences)
3. How it compares to the original product (similarities and differences)
4. Why someone might choose this alternative over the original product
After listing the alternatives, provide a brief explanation of your reasoning for
choosing these particular alternatives.
Present your response in the following format:
<alternatives>
<alternative1>
Name: [Product Name]
Description: [Brief description]
Comparison: [Similarities and differences]
Appeal: [Why someone might choose this alternative]
</alternative1>
[Repeat for each alternative]
<reasoning>
[Explanation of why you chose these alternatives]
</reasoning>
Changelog Blog
How-to Guides Community
▸
Sign in
Book a demo
Remember to consider a range of alternatives that might appeal to different
types of consumers or use cases related to the original product.
Note: This might require you to connect your chatbot to Google or a search engine for better and
updated results.
What are the best prompts you like using?
Stay updated on Linkedin for more Godmode news & updates.
in Stay updated
Request early access
Make revenue easy
Build 5x more relationships with personal
outreach
Request access
godmode
Blog Changelog Community
godmode
Changelog Blog How-to Guides Community
▸
Sign in
Book a demo
X
in
Privacy Policy Fulfilment Policy Terms of Service
