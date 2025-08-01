# Crisis Response Team Guide - Ash NLP v3.0

**A comprehensive guide for crisis response teams using the Three Zero-Shot Model Ensemble system**

---

## 🎯 Quick Start for Crisis Response Teams

### What is Ash NLP v3.0?

Ash NLP v3.0 is an AI system that **automatically analyzes Discord messages** to detect potential mental health crises. Instead of relying on a single AI model, it uses **three specialized models** that work together to provide:

- **More accurate crisis detection** (75% vs 61% accuracy)
- **Fewer false alarms** (8% vs 15% false positive rate)
- **Smart escalation** when the AI is uncertain
- **Transparent reasoning** for every decision

### How It Helps Your Team

✅ **Catches crises you might miss** - Works 24/7 monitoring all channels  
✅ **Reduces alert fatigue** - 47% fewer false alarms  
✅ **Provides context** - Shows exactly why it flagged a message  
✅ **Escalates uncertainty** - Asks for human review when models disagree  
✅ **Respects privacy** - Analyzes messages in real-time, doesn't store them  

---

## 🧠 Understanding the Three-Model System

### The Three AI Models

Think of it like having **three specialists** reviewing each message:

#### 1. 🧠 Depression Specialist (Primary)
- **What it does**: Looks for clinical signs of depression and suicidal ideation
- **Training**: Specialized in mental health language patterns
- **Strength**: Very good at detecting serious depression indicators
- **Weakness**: May miss non-clinical expressions of distress

#### 2. 💭 Sentiment Specialist (Context)
- **What it does**: Analyzes emotional tone and context
- **Training**: Understands social media language and expressions
- **Strength**: Catches emotional distress in casual language
- **Weakness**: May overreact to dramatic expressions

#### 3. 😰 Distress Specialist (Validation)
- **What it does**: Detects general emotional distress signals
- **Training**: Recognizes stress and emotional crisis patterns
- **Strength**: Good at identifying emotional overwhelm
- **Weakness**: Less specific about mental health vs general stress

### How They Work Together

```
Message: "I'm feeling really down and hopeless"

🧠 Depression Model: "moderate depression" (60% confidence)
💭 Sentiment Model: "negative" (90% confidence)
😰 Distress Model: "negative distress" (99% confidence)

✅ All agree it's a crisis → HIGH CONFIDENCE response
```

```
Message: "This exam is killing me but I can handle it"

🧠 Depression Model: "not depression" (96% confidence) ← "I can handle it"
💭 Sentiment Model: "negative" (69% confidence) ← "killing me"
😰 Distress Model: "negative distress" (93% confidence) ← mixed signals

⚠️ Models disagree → FLAGS FOR HUMAN REVIEW
```

---

## 🚨 Crisis Levels Explained

### The Four Crisis Levels

#### 🔴 HIGH Crisis
- **When**: All models agree on severe crisis indicators
- **Examples**: Clear suicidal ideation, immediate danger expressions
- **Action**: Immediate response required, automatic alert
- **Staff Role**: Respond within minutes

#### 🟡 MEDIUM Crisis  
- **When**: Models mostly agree on moderate crisis signs
- **Examples**: Depression expressions, hopelessness, self-harm hints
- **Action**: Response recommended, monitoring increased
- **Staff Role**: Reach out within hours

#### 🟠 LOW Crisis
- **When**: Some crisis indicators but mild or uncertain
- **Examples**: Stress expressions, mild depression language
- **Action**: Keep monitoring, gentle check-in
- **Staff Role**: Optional outreach, increased awareness

#### 🟢 NONE (Safe)
- **When**: No crisis indicators detected
- **Examples**: Normal conversation, positive expressions
- **Action**: No immediate action needed
- **Staff Role**: Continue normal community interaction

### Special Cases

#### ⚠️ **GAP DETECTED** (Requires Review)
- **When**: Models significantly disagree on crisis level
- **Why Important**: Indicates complex or ambiguous language
- **Examples**: Sarcasm, idioms, mixed emotional messages
- **Staff Role**: **HUMAN REVIEW REQUIRED** - Use your judgment

---

## 📊 Reading AI Analysis Reports

### Standard Analysis Response

```json
{
  "crisis_level": "medium",
  "confidence_score": 0.70,
  "needs_response": true,
  "processing_time_ms": 31,
  "reasoning": "Context shows no humor or positive indicators. Strong negative sentiment detected. Depression model indicates moderate risk."
}
```

**Key Fields for Teams**:
- **`crisis_level`**: The final decision (high/medium/low/none)
- **`needs_response`**: Whether team action is recommended
- **`confidence_score`**: How certain the AI is (0.0 - 1.0)
- **`reasoning`**: Human-readable explanation of the decision

### Ensemble Analysis Response

```json
{
  "ensemble_analysis": {
    "predictions": {
      "depression": "moderate",
      "sentiment": "negative", 
      "emotional_distress": "NEGATIVE"
    },
    "confidence_scores": {
      "depression": 0.60,
      "sentiment": 0.90,
      "emotional_distress": 0.99
    },
    "gaps_detected": false,
    "consensus": {
      "prediction": "NEGATIVE",
      "confidence": 0.70,
      "method": "unanimous_consensus"
    }
  },
  "requires_staff_review": false,
  "crisis_level": "medium"
}
```

**Key Fields for Teams**:
- **`gaps_detected`**: Whether models disagreed (if `true`, review needed)
- **`requires_staff_review`**: AI recommendation for human review
- **`consensus.method`**: How the decision was made
- **`predictions`**: What each individual model thought

---

## 🔍 Gap Detection: When AI Needs Help

### What is Gap Detection?

Gap detection happens when the three AI models **disagree significantly** about a message. This is actually a **feature, not a bug** - it means the AI recognized that human judgment is needed.

### Types of Gaps

#### 1. **Meaningful Disagreement**
```json
{
  "type": "meaningful_disagreement",
  "crisis_models": ["sentiment", "emotional_distress"],
  "safe_models": ["depression"]
}
```
- **What it means**: Some models see crisis, others see safety
- **Example**: "This test is killing me but I've got this!"
- **Your role**: Use context knowledge to decide

#### 2. **Confidence Disagreement**
```json
{
  "type": "confidence_disagreement", 
  "spread": 0.65,
  "threshold": 0.5
}
```
- **What it means**: Models agree on prediction but confidence varies widely
- **Example**: Unclear sarcasm or cultural references
- **Your role**: Consider community context and user history

### When You See Gap Detection

✅ **DO**: 
- Review the message with full context
- Consider the user's recent activity and relationships
- Use your community knowledge
- Trust your human instincts
- Document your decision for learning

❌ **DON'T**:
- Automatically assume it's not a crisis
- Ignore the AI completely
- Rush to judgment without context
- Treat gap detection as system failure

---

## 🎯 Best Practices for Crisis Response Teams

### Daily Workflow

#### 1. **Morning Setup** (5 minutes)
```bash
# Check system health
curl http://localhost:8881/health

# Review overnight statistics  
curl http://localhost:8881/stats
```

#### 2. **Active Monitoring**
- **High/Medium alerts**: Respond according to your protocols
- **Gap detection alerts**: Review within 2-4 hours
- **System status**: Monitor dashboard for unusual patterns

#### 3. **End of Day Review** (10 minutes)
- Review any gap detection cases
- Check for missed patterns
- Note any new community language/expressions

### Response Guidelines

#### For HIGH Crisis Alerts
1. **Immediate Action** (within 5 minutes)
2. **Read AI reasoning** to understand what triggered it
3. **Check user context** (recent messages, relationships)
4. **Follow your standard crisis protocol**
5. **Document outcome** for system learning

#### For MEDIUM Crisis Alerts  
1. **Timely Response** (within 2 hours)
2. **Gentle outreach** or increased monitoring
3. **Consider community context**
4. **Escalate if needed**

#### For Gap Detection Cases
1. **Human Review Required** (within 4 hours)
2. **Read all three model predictions**
3. **Consider why models disagreed**
4. **Make informed decision** based on full context
5. **Provide feedback** to improve system

### Escalation Procedures

#### When to Override AI Decisions

**Override to Higher Crisis Level** when:
- You know additional context the AI missed
- User has history of minimizing their struggles  
- Community patterns suggest higher risk
- Your intuition strongly disagrees

**Override to Lower Crisis Level** when:
- Clear sarcasm or humor the AI missed
- Cultural/community expressions AI doesn't understand
- Context clearly indicates safety
- False positive patterns you recognize

#### Documentation

For each override, note:
- **Original AI decision and confidence**
- **Your decision and reasoning** 
- **Context the AI missed**
- **Outcome** (for learning)

---

## 🛠️ Tools and Resources

### Quick Access URLs

Bookmark these for daily use:

```bash
# System health check
http://localhost:8881/health

# Service statistics
http://localhost:8881/stats

# Learning system status
http://localhost:8881/learning_statistics
```

### Useful Commands

#### Test Message Analysis
```bash
# Quick test
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "TEST MESSAGE HERE", "user_id": "test", "channel_id": "test"}'

# Full ensemble analysis
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "TEST MESSAGE HERE", "user_id": "test", "channel_id": "test"}'
```

### Dashboard Integration

If you have Ash Dashboard access:
- **Real-time alerts**: Live crisis detection notifications
- **Gap analysis**: Visual representation of model disagreements
- **Trend analysis**: Patterns in community mental health
- **Performance metrics**: AI accuracy and response times

---

## 📚 Understanding AI Limitations

### What the AI Does Well

✅ **Consistent 24/7 monitoring**  
✅ **Rapid analysis** (sub-35ms response times)  
✅ **Pattern recognition** across large amounts of text  
✅ **Objective evaluation** without fatigue or bias  
✅ **Multiple perspective analysis** through ensemble  

### What Requires Human Judgment

❌ **Complex social context** and relationship dynamics  
❌ **Cultural nuances** and community-specific language  
❌ **Sarcasm and humor** in crisis expressions  
❌ **Historical context** about individual users  
❌ **Situational awareness** beyond the message text  

### Working Together Effectively

The AI is your **augmentation, not replacement**:

- **AI strength**: Consistent, fast, pattern-based detection
- **Human strength**: Context, relationships, cultural understanding
- **Together**: More comprehensive crisis prevention

---

## 🚨 Emergency Procedures

### If AI System Goes Down

1. **Immediate**: Switch to manual monitoring protocols
2. **Check**: System health endpoint for status
3. **Contact**: Technical team via Discord or GitHub issues  
4. **Document**: What messages might have been missed
5. **Resume**: Gradual re-integration when system restored

### If AI Accuracy Drops

Signs to watch for:
- Sudden increase in false positives/negatives
- Many gap detection cases
- Team overriding most decisions

**Actions**:
1. Document patterns you're seeing
2. Contact technical team with examples
3. Continue using human judgment
4. Provide feedback for system improvement

### Data Privacy Incidents

**Remember**: 
- AI analyzes messages in real-time only
- No message content is stored permanently
- Only analysis results are logged
- User privacy is protected by design

If concerned about privacy:
1. Check system logs for data retention
2. Contact technical team immediately
3. Document the concern
4. Follow your organization's privacy protocols

---

## 📈 Performance Monitoring

### Key Metrics to Track

#### Accuracy Metrics
- **True Positives**: Correctly identified crises
- **False Positives**: Incorrectly flagged non-crises  
- **True Negatives**: Correctly identified safe messages
- **False Negatives**: Missed actual crises

#### Response Metrics
- **Response Time**: How quickly you respond to alerts
- **Override Rate**: How often you disagree with AI
- **Gap Resolution**: How you handle model disagreements
- **Outcome Tracking**: Results of interventions

#### System Metrics
- **Processing Speed**: AI response times
- **Uptime**: System availability
- **Memory Usage**: Resource consumption
- **Model Agreement**: How often models consensus

### Monthly Review Process

1. **Gather Statistics** from dashboard/API
2. **Analyze Patterns** in AI decisions and team responses
3. **Identify Issues** such as recurring false positives
4. **Plan Improvements** in process or system configuration
5. **Document Lessons** learned for team training

---

## 🎓 Training and Onboarding

### New Team Member Checklist

#### Week 1: Understanding
- [ ] Read this guide completely
- [ ] Understand the three-model concept
- [ ] Learn crisis level meanings
- [ ] Practice with test messages

#### Week 2: Observation
- [ ] Shadow experienced team members
- [ ] Observe gap detection cases
- [ ] Practice using dashboard tools
- [ ] Learn escalation procedures

#### Week 3: Guided Practice
- [ ] Handle low-priority alerts with supervision
- [ ] Make decisions on gap detection cases
- [ ] Practice documentation
- [ ] Learn override procedures

#### Week 4: Independent Practice
- [ ] Handle alerts independently
- [ ] Demonstrate understanding of AI limitations
- [ ] Show good judgment in override situations
- [ ] Complete certification assessment

### Ongoing Education

#### Monthly Training Topics
- **New community language patterns**
- **Emerging crisis indicators**  
- **AI system updates and improvements**
- **Case studies from gap detection reviews**
- **Mental health best practices**

#### Resources for Learning
- **Crisis intervention training**
- **LGBTQIA+ cultural competency**
- **AI/ML basics for non-technical users**
- **Community-specific support techniques**

---

## 🤝 Feedback and Improvement

### How Your Feedback Improves the System

Every time you:
- **Override an AI decision** → Helps train future versions
- **Document gap detection reasoning** → Improves consensus algorithms  
- **Report new language patterns** → Expands detection capabilities
- **Share outcome data** → Validates system effectiveness

### Feedback Collection

#### Daily Feedback
- Override decisions with reasoning
- Gap detection case resolutions  
- New expressions/language noted
- System performance observations

#### Weekly Feedback
- Pattern summaries
- Accuracy observations
- Suggested improvements
- Training needs identified

#### Monthly Feedback
- Comprehensive performance review
- System enhancement suggestions
- Process improvement ideas
- Community needs assessment

### Continuous Improvement Process

1. **Collect**: Team feedback and system metrics
2. **Analyze**: Patterns and improvement opportunities
3. **Prioritize**: Most impactful enhancements
4. **Implement**: System and process updates
5. **Validate**: Improved performance with team
6. **Document**: Changes and lessons learned

---

## 📞 Support and Resources

### Technical Support

**Discord**: [#ash-support](https://discord.gg/alphabetcartel)  
**GitHub Issues**: [Report bugs/requests](https://github.com/the-alphabet-cartel/ash-nlp/issues)  
**Documentation**: [Technical API docs](../tech/api_v3_0.md)  

### Mental Health Resources

**Crisis Lines**: Always available for immediate support  
**Community Resources**: LGBTQIA+ specific mental health services  
**Training Materials**: Crisis intervention and suicide prevention  
**Best Practices**: Community mental health support techniques  

### Community Support

**The Alphabet Cartel**: [Discord community](https://discord.gg/alphabetcartel)  
**Website**: [alphabetcartel.org](http://alphabetcartel.org)  
**Other Crisis Response Teams**: Connect with peer organizations  

---

**🏳️‍🌈 Remember: Technology amplifies human compassion - you are the heart of this system.**

*This guide is living document. Please contribute your experiences and suggestions to help other crisis response teams serve their communities more effectively.*