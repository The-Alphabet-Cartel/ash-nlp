<!-- ash-nlp/docs/team/team_guide.md -->
<!--
API Guide for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Crisis Response Team Guide

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# Crisis Response Team Operational Guide

Comprehensive guide for crisis response teams using Ash-NLP v3.1 for LGBTQIA+ community mental health support.

---

## Understanding Ash-NLP v5.0

### What is Ash-NLP?
Ash-NLP v5.0 is an AI-powered crisis detection system specifically designed for LGBTQIA+ Discord communities. It analyzes messages in real-time to identify potential mental health crises and alerts trained crisis response team members when intervention may be needed.

### Core Capabilities
- **Real-time analysis** of Discord messages with 147ms average response time
- **Multi-level crisis classification** from low to critical severity
- **LGBTQIA+-aware pattern recognition** understanding community-specific language
- **Adaptive learning** from feedback to improve accuracy over time
- **Confidence scoring** indicating system certainty in its assessments

---

## Crisis Classification System

### Crisis Levels

#### None (Score: {TBD})
- **Description**: No crisis indicators detected
- **Action**: Continue normal community monitoring
- **Example Messages**: "Having a great day!", "Thanks for the help"

#### Low (Score: {TBD})
- **Description**: Mild distress or negative emotions
- **Action**: Monitor for escalation, consider check-in
- **Example Messages**: "Feeling a bit down today", "Work is stressful"
- **Response**: Gentle community support, resources sharing

#### Medium (Score: {TBD})
- **Description**: Moderate distress requiring attention
- **Action**: Direct intervention recommended
- **Example Messages**: "I don't know how to cope anymore", "Everything feels overwhelming"
- **Response**: Personal outreach, emotional support, resource connection

#### High (Score: {TBD})
- **Description**: Significant crisis indicators present
- **Action**: Immediate intervention required
- **Example Messages**: "I can't take this anymore", "Nothing matters"
- **Response**: Direct contact, crisis resources, potential professional referral

#### Critical (Score: {TBD})
- **Description**: Severe crisis with potential immediate risk
- **Action**: Emergency intervention protocol
- **Example Messages**: "I want to end it all", "Goodbye everyone"
- **Response**: Immediate crisis intervention, professional resources, emergency protocols

---

## Response Protocols

### Immediate Response Framework

#### 1. Assessment Phase (0-2 minutes)
- **Review AI Analysis**: Check crisis score, confidence level, and detected categories
- **Message Context**: Read full message and recent conversation history
- **User History**: Consider user's previous interactions and known circumstances
- **Confidence Evaluation**: Higher confidence scores warrant more immediate action

#### 2. Initial Contact (2-5 minutes)
- **Direct Message**: Reach out privately to avoid public attention
- **Empathetic Opening**: "I noticed you might be going through something difficult"
- **Non-judgmental Approach**: Avoid assumptions about user's experience
- **Availability Check**: "Would you like to talk about what's happening?"

#### 3. Support Provision (5-30 minutes)
- **Active Listening**: Allow user to share without interruption
- **Validation**: Acknowledge their feelings and experiences
- **Resource Sharing**: Provide relevant crisis resources and support contacts
- **Safety Assessment**: Evaluate immediate safety concerns

#### 4. Follow-up Planning (30+ minutes)
- **Continued Support**: Schedule check-ins as appropriate
- **Community Connection**: Help connect user with ongoing support
- **Documentation**: Record intervention details for team coordination
- **Professional Referral**: Facilitate connection to professional services if needed

### Response Templates

#### Initial Outreach - Medium Crisis
```
Hi [Username],

I noticed you mentioned feeling overwhelmed. I want you to know that you're not alone, and it's okay to reach out when things feel difficult.

Would you like to talk about what's going on? I'm here to listen without judgment, and we can explore some resources that might help.

Take care,
[Your Name] - Crisis Response Team
```

#### Initial Outreach - High Crisis
```
Hi [Username],

I saw your message and I'm concerned about you. What you're going through sounds really difficult, and I want you to know that your feelings are valid.

You don't have to face this alone. Would you be willing to chat for a few minutes? I'm here to listen and help connect you with support if you'd like.

Your life has value, and there are people who care about you.

[Your Name] - Crisis Response Team
```

#### Critical Crisis Response
```
[Username], 

I'm very concerned about your message. I want you to know that you matter, and there are people who want to help you through this difficult time.

Please reach out to me immediately. If you're in immediate danger, please contact:
- Emergency Services: 988 (Suicide & Crisis Lifeline)
- Text HOME to 741741 (Crisis Text Line)
- Emergency Services: 911

You are not alone. We care about you.

URGENT - [Your Name] - Crisis Response Team
```

---

## Understanding AI Analysis

### Analysis Components

#### Crisis Score Interpretation
- **{TBD}**: Background monitoring sufficient
- **{TBD}**: Increased attention warranted
- **{TBD}**: Direct outreach recommended
- **{TBD}**: Immediate intervention needed
- **{TBD}**: Emergency protocols activated

#### Confidence Score Meaning
- **{TBD}**: Very high confidence - trust AI assessment
- **{TBD}**: Good confidence - verify with context review
- **{TBD}**: Moderate confidence - human judgment crucial
- **{TBD}**: Low confidence - requires careful evaluation
- **{TBD}**: Very low confidence - likely false positive

#### Detected Categories
- **emotional_distress**: General emotional pain or suffering
- **depression_indicators**: Signs of depressive thoughts or feelings
- **anxiety_patterns**: Anxiety-related expressions
- **isolation_indicators**: Signs of social withdrawal or loneliness
- **self_harm_risk**: Potential self-harm indicators
- **suicidal_ideation**: Suicide-related thoughts or expressions

### AI Model Details
The system uses three AI models working together:
- **Model 1**: {TBD}
- **Model 2**: {TBD}
- **Model 3**: {TBD}

---

## LGBTQIA+ Specific Considerations

### Community-Aware Response

#### Identity Affirmation
- **Use correct pronouns** as stated in user profiles or previous conversations
- **Respect chosen names** and identity expressions
- **Avoid assumptions** about sexual orientation or gender identity
- **Validate LGBTQIA+ experiences** as legitimate and important

#### Community Stressors
- **Coming out stress** and family rejection concerns
- **Discrimination experiences** in work, school, or community settings
- **Identity exploration** and questioning periods
- **Medical transition** stress and healthcare access issues
- **Community belonging** and acceptance concerns

#### Specialized Resources
Maintain connections to LGBTQIA+-specific crisis resources:
- **The Trevor Project**: 1-866-488-7386 (LGBTQ youth crisis support)
- **Trans Lifeline**: 877-565-8860 (transgender crisis support)
- **LGBT Hotline**: 1-888-843-4564 (general LGBTQ support)
- **Local LGBTQIA+ community centers** and support groups

### Language Sensitivity

#### Affirming Language
- "Your identity is valid"
- "You belong in this community"
- "Your experiences matter"
- "You deserve love and acceptance"

#### Avoid These Phrases
- "Have you tried just being more positive?"
- "It's just a phase"
- "Things could be worse"
- "Everyone goes through this"

---

## Team Coordination

### Case Documentation

#### Required Information
- **Timestamp** of initial alert and intervention
- **Crisis level** and confidence score from AI analysis
- **User identifier** (maintain privacy appropriately)
- **Intervention actions** taken
- **Outcome** and current status
- **Follow-up** plans or requirements

#### Documentation Template
```
Crisis Intervention Log

Date/Time: [timestamp]
User: [identifier]
Crisis Level: [level] (Score: [score], Confidence: [confidence])

AI Analysis:
- Detected Categories: [categories]
- Model Agreement: [consensus/disagreement]
- Processing Time: [ms]

Intervention:
- Initial Contact: [time]
- Response Method: [DM/channel/voice]
- Duration: [minutes]
- Resources Provided: [list]

Outcome:
- Immediate Safety: [secured/ongoing concern]
- User Response: [positive/neutral/no response]
- Professional Referral: [yes/no - details]
- Follow-up Needed: [yes/no - when]

Team Member: [name]
```

---

## Emergency Protocols

### Immediate Danger Assessment

#### High-Risk Indicators
- **Specific suicide plans** with means and timeline
- **Imminent self-harm** statements
- **Goodbye messages** to community
- **Active substance use** during crisis
- **Complete isolation** from support systems

#### Emergency Actions
1. **Immediate engagement** - do not delay response
2. **Stay online** with the user if possible
3. **Encourage professional contact** - provide crisis line numbers
4. **Contact emergency services** if user shares location and imminent danger
5. **Team alert** - notify other team members immediately
6. **Document everything** for follow-up and learning

### Crisis Resource Quick Reference

#### National Resources
- **988 Suicide & Crisis Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **National Sexual Assault Hotline**: 1-800-656-4673

#### LGBTQIA+ Specific
- **The Trevor Project**: 1-866-488-7386
- **Trans Lifeline**: 877-565-8860
- **LGBTQ National Hotline**: 1-888-843-4564

#### International
- **UK Samaritans**: 116 123
- **Canada Talk Suicide**: 1-833-456-4566
- **Australia Lifeline**: 13 11 14

---

## Training and Development

### Required Competencies

#### Technical Skills
- **AI system understanding** - interpreting analysis results
- **Platform proficiency** - Discord navigation and features
- **Documentation practices** - accurate case recording
- **Resource navigation** - quick access to crisis resources

#### Crisis Intervention Skills
- **Active listening** and empathetic communication
- **De-escalation techniques** for high-stress situations
- **Safety assessment** and risk evaluation
- **Cultural competency** for LGBTQIA+ community needs
- **Trauma-informed care** principles

### Ongoing Development

#### Monthly Training Topics
- **LGBTQIA+ mental health** specific challenges and resources
- **Crisis intervention** technique refinement
- **AI system updates** and new features
- **Community feedback** integration and protocol updates
- **Self-care** and team support strategies

#### Self-Care for Team Members

#### Stress Management
- **Regular breaks** during shifts
- **Peer support** and debriefing opportunities
- **Professional counseling** resources for team members
- **Workload management** to prevent burnout

#### Boundaries
- **Clear shift limits** to maintain personal wellbeing
- **Emotional boundaries** while maintaining empathy
- **Professional support** for challenging cases
- **Team backup** systems for overwhelming situations

---

## System Administration

### Monitoring AI Performance

#### Daily Checks
- **System health status** via `/health` endpoint
- **Response time trends** and performance metrics
- **False positive/negative** rates from team feedback
- **Learning system** adjustment activity

#### Weekly Reviews
- **Performance analysis** with full team
- **Threshold adjustments** based on community patterns
- **Protocol effectiveness** evaluation
- **Resource utilization** assessment

### Threshold Management

#### Understanding Thresholds
Current crisis detection thresholds:
- **Low**: {TBD}
- **Medium**: {TBD}
- **High**: {TBD}
- **Critical**: {TBD}

#### When to Adjust
- **High false positive rate** - consider raising thresholds
- **Missing real crises** - consider lowering thresholds
- **Community feedback** indicating over/under-sensitivity
- **Seasonal patterns** or community events affecting baseline

---

## Conclusion

This guide provides the foundation for effective crisis response using Ash-NLP v5.0. Remember that the AI system is a tool to assist human judgment, not replace it. Your expertise, empathy, and understanding of the LGBTQIA+ community remain the most critical elements in providing life-saving support.

### Key Principles
1. **Human judgment** remains paramount in all crisis situations
2. **Community understanding** enhances the effectiveness of AI analysis
3. **Continuous learning** improves both human and AI performance
4. **Team support** enables sustainable crisis response operations
5. **User safety** is always the highest priority

The combination of advanced AI assistance and skilled human intervention creates a powerful system for supporting LGBTQIA+ community mental health and crisis prevention.

---

*Crisis Response Team Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
