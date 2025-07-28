# Ash NLP Server - Crisis Response Team Guide v2.1

**Operations Guide for Crisis Response Teams**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🎯 Overview

This guide provides crisis response teams with essential information about how the Ash NLP Server enhances our community's crisis detection and support capabilities.

### What Is the NLP Server?

The Ash NLP Server is an advanced artificial intelligence system that analyzes Discord messages in real-time to identify potential mental health crises, self-harm indicators, and community members who may need support.

**Key Capabilities:**
- **Real-time Analysis**: Every message is analyzed within 200ms
- **Risk Classification**: Categorizes concerns as High, Medium, or Low priority
- **Context Understanding**: Distinguishes between gaming frustration and genuine crisis
- **Learning System**: Continuously improves based on team feedback
- **Privacy Protection**: No messages are stored permanently

## 🚨 Crisis Detection System

### Risk Level Classifications

**🔴 High Crisis (Immediate Response Required)**
- **Score Range**: 0.50 - 1.00
- **Response Time**: Immediate (within 5 minutes)
- **Indicators**: 
  - Suicidal ideation ("I want to die", "ending it all")
  - Self-harm references ("cutting myself", "hurting myself")
  - Immediate danger signals ("tonight is the night", "goodbye everyone")
  - Crisis escalation language ("can't take it anymore", "no point living")

**🟡 Medium Crisis (Close Monitoring)**
- **Score Range**: 0.22 - 0.49
- **Response Time**: Within 30 minutes
- **Indicators**:
  - Depression markers ("everything is hopeless", "nothing matters")
  - Anxiety indicators ("panic attacks", "can't breathe")
  - Social isolation ("nobody understands", "completely alone")
  - Identity struggles ("hate who I am", "don't belong anywhere")

**🟢 Low Crisis (Supportive Check-in)**
- **Score Range**: 0.12 - 0.21
- **Response Time**: Within 2 hours
- **Indicators**:
  - Mild mood indicators ("feeling down", "rough day")
  - Stress signals ("overwhelmed", "too much pressure")
  - Gaming frustration ("this game is killing me")
  - General support needs ("need someone to talk to")

### Understanding Detection Accuracy

**Current Performance Metrics:**
- **Overall Accuracy**: 87%
- **High Crisis Detection**: 96% (rarely misses serious situations)
- **False Positive Rate**: 6.2% (low rate of false alarms)
- **Average Analysis Time**: 145ms

**What This Means:**
- The system correctly identifies 96% of high-crisis situations
- About 1 in 16 alerts may be false positives (still worth checking)
- Very rare to miss genuine high-priority situations
- Gaming language usually distinguished from real crisis talk

## 🔄 Learning & Feedback System

### How the Learning System Works

The NLP server continuously learns from team feedback to improve its accuracy and reduce false positives/negatives.

**Feedback Types:**
1. **False Positive**: System flagged a message that wasn't actually concerning
2. **False Negative**: System missed a message that should have been flagged
3. **Correct Classification**: System got it right (reinforces good behavior)
4. **Severity Adjustment**: Right category but wrong priority level

### Providing Feedback

**Through Ash Dashboard:**
1. Review flagged messages in the dashboard
2. Click "Provide Feedback" next to any detection
3. Select feedback type and correct classification
4. Add optional notes about why the detection was incorrect
5. Submit feedback

**Through Discord Commands:**
```
!ash feedback <message_id> false_positive
!ash feedback <message_id> false_negative high_crisis
!ash feedback <message_id> correct
!ash feedback <message_id> adjust medium_crisis
```

**Best Practices for Feedback:**
- **Be Timely**: Provide feedback within 24 hours when possible
- **Be Specific**: Include context about why classification was wrong
- **Focus on Patterns**: Note recurring issues (e.g., specific gaming terminology)
- **Document Context**: Include information about user's typical communication style

### Learning Impact

**Real-time Improvements:**
- Feedback is processed immediately
- Model adjustments applied within 10-15 minutes
- Changes affect future analysis of similar messages
- Learning is preserved across server restarts

**Weekly Learning Reports:**
Teams receive weekly reports showing:
- Number of feedback submissions
- Classification improvements
- Accuracy trend changes
- Identified new language patterns

## 📊 Working with Ash Dashboard

### Dashboard Access

**URL**: https://dashboard.alphabetcartel.net  
**Backup URL**: http://10.20.30.253:8883

**Team Member Accounts:**
All crisis response team members should have dashboard accounts. Contact admin if you need access.

### Key Dashboard Features

**Real-time Crisis Feed:**
- Live stream of detected potential crises
- Color-coded by severity level
- One-click response actions
- Message context and user history

**Analytics & Trends:**
- Detection accuracy over time
- False positive/negative rates
- Response time metrics
- Community mental health trends

**Team Performance:**
- Response time tracking
- Intervention outcomes
- Feedback contribution metrics
- Team coordination tools

**Learning System Monitor:**
- Current model performance
- Recent learning adjustments
- Feedback processing status
- System health indicators

### Daily Workflow Integration

**Morning Check (Start of Shift):**
1. Review overnight detection summary
2. Check any high-priority flags that may need follow-up
3. Review learning system status
4. Note any system alerts or maintenance

**During Active Monitoring:**
1. Monitor real-time crisis feed
2. Respond to alerts according to priority levels
3. Use dashboard tools for user context and history
4. Coordinate with team members through dashboard chat

**End of Shift:**
1. Provide feedback on handled cases
2. Document any concerning patterns
3. Update case notes in dashboard
4. Brief incoming team on active situations

## 🔧 Technical Understanding for Teams

### System Architecture

**NLP Server (10.20.30.16:8881):**
- Windows 11 server with NVIDIA RTX 3050
- Processes ~1000 messages per minute
- Maintains 99.5% uptime
- Automatic failover to backup systems

**Integration Points:**
- **Ash Bot**: Sends messages for analysis
- **Dashboard**: Displays results and analytics
- **Testing Suite**: Validates system accuracy

### Performance Monitoring

**Key Metrics to Watch:**
- **Response Time**: Should be <200ms average
- **Accuracy Rate**: Should be >85% overall
- **High Crisis Detection**: Should be >95%
- **System Uptime**: Should be >99%

**Warning Signs:**
- Response times consistently >500ms
- Accuracy dropping below 80%
- Unusual number of false positives
- System health alerts in dashboard

### What to Do When Systems Are Down

**Immediate Actions:**
1. **Don't Panic**: Manual monitoring procedures are in place
2. **Increase Vigilance**: Watch channels more carefully for concerning messages
3. **Use Backup Tools**: Manual keyword monitoring still functions
4. **Report Issues**: Notify tech team immediately via Discord

**Backup Procedures:**
```
Manual Crisis Keywords to Watch:
High Priority: suicide, kill myself, end it all, can't go on, 
               cutting, self harm, goodbye everyone, tonight
Medium Priority: hopeless, alone, nobody cares, hate myself,
                 depressed, anxiety, panic attack
```

## 👥 Team Coordination

### Communication Protocols

**Crisis Response Coordination:**
- **#crisis-response**: Primary team coordination channel
- **#crisis-alerts**: Automated system alerts and high-priority flags
- **#team-feedback**: Discuss detection accuracy and improvements

**Escalation Procedures:**
1. **Level 1**: Team member response (most situations)
2. **Level 2**: Senior team member involvement (complex situations)
3. **Level 3**: Professional resources (emergency situations)
4. **Emergency**: 911/crisis hotlines (immediate danger)

### Role-Specific Guidelines

**Primary Responders:**
- Monitor real-time feeds during assigned shifts
- Respond to High/Medium crisis alerts
- Provide initial assessment and intervention
- Document interventions in dashboard

**Senior Team Members:**
- Review complex or escalated cases
- Provide guidance on difficult assessments
- Coordinate with professional resources
- Train new team members

**Feedback Specialists:**
- Focus on system accuracy improvement
- Analyze false positive/negative patterns
- Work with tech team on detection improvements
- Maintain learning system quality

**Analytics Coordinators:**
- Monitor overall community mental health trends
- Generate weekly/monthly reports
- Identify systemic issues or patterns
- Coordinate with community leadership

## 📚 Training & Best Practices

### Onboarding for New Team Members

**Week 1: System Familiarization**
- Complete dashboard training
- Shadow experienced team members
- Practice using feedback systems
- Learn crisis classification criteria

**Week 2: Active Monitoring**
- Handle Low and Medium priority alerts
- Practice coordination protocols
- Begin providing system feedback
- Document learning experiences

**Week 3: Full Responsibilities**
- Handle all priority levels
- Take on training newer members
- Contribute to system improvements
- Participate in team coordination

### Ongoing Training Requirements

**Monthly Requirements:**
- 2 hours crisis response skill training
- 1 hour NLP system update training
- 30 minutes dashboard feature training
- Team coordination exercises

**Quarterly Requirements:**
- Mental health first aid refresher
- System accuracy review training
- Emergency procedure drills
- Professional development sessions

### Best Practice Guidelines

**Crisis Response:**
1. **Respond Promptly**: Meet response time targets
2. **Stay Calm**: Maintain professional demeanor
3. **Document Everything**: Record interventions and outcomes
4. **Follow Up**: Check on community members after interventions
5. **Seek Support**: Don't handle everything alone

**System Interaction:**
1. **Trust but Verify**: System is accurate but use human judgment
2. **Provide Feedback**: Help improve system accuracy
3. **Watch for Patterns**: Note recurring issues or improvements
4. **Stay Updated**: Keep current with system changes and updates

**Team Coordination:**
1. **Communicate Clearly**: Share relevant information with team
2. **Support Teammates**: Assist colleagues when needed
3. **Share Knowledge**: Help train new team members
4. **Take Breaks**: Prevent burnout through proper rest

## 🚨 Emergency Procedures

### System Emergency Responses

**NLP Server Down:**
1. Switch to manual monitoring mode
2. Increase team coverage in key channels
3. Use backup keyword detection
4. Notify all team members of status change
5. Coordinate with tech team for resolution

**Dashboard Unavailable:**
1. Use Discord-based coordination
2. Rely on direct message monitoring
3. Maintain manual documentation
4. Use phone/text for team coordination

**High Volume Crisis Events:**
1. Activate all available team members
2. Implement crisis triage protocols
3. Coordinate with external resources
4. Document event for post-incident review

### Personal Safety Protocols

**For Team Members:**
- Take regular breaks during intense periods
- Seek supervisor support for difficult cases
- Use employee assistance programs if available
- Recognize signs of secondary trauma

**Mandatory Reporting:**
- Threats of violence to others
- Child abuse indicators
- Elder abuse situations
- Legal obligations per local laws

## 📞 Support & Resources

### Technical Support
- **GitHub Issues**: System bugs and feature requests
- **Discord #tech-support**: Quick technical questions
- **Dashboard Help**: Built-in help system and tutorials

### Crisis Response Support
- **Team Supervisor**: Direct escalation for complex cases
- **Mental Health Professionals**: Consultation for difficult assessments
- **Emergency Services**: 911, crisis hotlines, mobile crisis teams

### Training Resources
- **Internal Documentation**: Complete team manual and procedures
- **External Training**: Mental health first aid, crisis intervention
- **Professional Development**: Conferences, workshops, certification programs

### Community Resources
- **Crisis Hotlines**: National Suicide Prevention Lifeline, local crisis centers
- **LGBTQIA+ Resources**: Trevor Project, PFLAG, local community centers
- **Gaming Support**: Specialized counselors familiar with gaming communities

---

## 🎯 Success Metrics

### Individual Performance
- **Response Time**: Meet priority-based response targets
- **Intervention Quality**: Positive outcomes and user feedback
- **System Feedback**: Regular, high-quality feedback submissions
- **Team Coordination**: Effective communication and collaboration

### Team Performance
- **Community Safety**: Reduced crisis escalation rates
- **System Accuracy**: Improved detection through feedback
- **Response Coverage**: 24/7 monitoring with appropriate staffing
- **Professional Development**: Ongoing skill improvement and training

### System Impact
- **Detection Accuracy**: Continuous improvement in AI performance
- **Community Trust**: Members feel safe and supported
- **Early Intervention**: Preventing crises before they escalate
- **Resource Connection**: Successfully linking members to appropriate help

---

## 🌈 Remember Our Mission

**The Alphabet Cartel exists to create safe, inclusive gaming communities where everyone can be their authentic selves.**

The Ash NLP Server is a tool that helps us fulfill this mission by:
- Identifying community members who need support
- Enabling faster, more accurate crisis response
- Creating a safety net for our most vulnerable members
- Building a community where mental health is prioritized

**Every interaction matters. Every detection could save a life. Every piece of feedback makes our community safer.**

---

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*"We've all been in that dark place where everything feels impossible. You're not alone."* - Ash

**Built with 🖤 for chosen family everywhere.**