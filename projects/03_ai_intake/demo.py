"""Mock rules only; no live LLM, training, real records or inference API."""
import json
class ReviewFirstDemo:
    def decide(self,text):
        if not isinstance(text,str) or len(text.strip())<2:raise ValueError('invalid text')
        lower=text.lower()
        category='billing' if 'invoice' in lower else 'general' if 'hello' in lower else 'unknown'
        status='manual_review' if category!='general' else 'draft_only'
        return {'category':category,'status':status,'provider':'local-rule-mock','human_approval_required':status=='manual_review'}
if __name__=='__main__':print(json.dumps(ReviewFirstDemo().decide('Please review invoice'),sort_keys=True))
