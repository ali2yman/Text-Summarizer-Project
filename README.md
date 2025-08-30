# 🎫 Ticket Data Summary & Analysis App

A Streamlit application that processes system ticket data and generates AI-powered storytelling summaries using Google Gemini AI.

      https://ali2yman-text-summarizer-project-main-7hlwsl.streamlit.app/

## 📋 Features

- **File Processing**: Upload TXT, CSV, or XLSX files
- **Data Cleaning**: Automatic filtering and preprocessing 
- **AI Summaries**: Generate storytelling summaries using Gemini AI
- **Analytics Dashboard**: Visual charts and business insights
- **Export Options**: Download processed data and reports

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project files
# Navigate to project directory

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key (you'll need it in the app)

### 3. Run the Application

```bash
streamlit run main.py
```

## 📁 Project Structure

```
ticket-summary-app/
├── main.py              # Main Streamlit application
├── config.py            # Configuration settings
├── data_processor.py    # Data processing functions
├── story_generator.py   # AI story generation
├── visualization.py     # Charts and analytics
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## 💾 File Format Requirements

Your ticket data file must contain these columns:

- `ORDER_NUMBER` - Unique ticket identifier
- `ACCEPTANCE_TIME` - When ticket was created (MM/DD/YYYY HH:MM)
- `COMPLETION_TIME` - When ticket was resolved
- `CUSTOMER_NUMBER` - Customer identifier
- `SERVICE_CATEGORY` - Must be one of: HDW, NET, KAI, KAV, GIGA, VOD, KAD
- `ORDER_DESCRIPTION_1` - Primary issue description
- `ORDER_DESCRIPTION_2` - Secondary issue description
- `COMPLETION_RESULT_KB` - Resolution details
- `NOTE_MAXIMUM` - Additional notes

## 🏷️ Product Categories

| Category | Product    | Description |
|----------|------------|-------------|
| NET, KAI | Broadband  | Internet services |
| KAV      | Voice      | Phone services |
| KAD      | TV         | Television services |
| GIGA     | GIGA       | High-speed internet |
| VOD      | VOD        | Video on demand |
| HDW      | Hardware   | Hardware issues |

## 📖 Story Sections

Each AI-generated summary includes 5 chronological sections:

1. **Initial Issue** - First reported problems and immediate actions
2. **Follow-ups** - Response activities and customer interactions  
3. **Developments** - Progress made and evolving situations
4. **Later Incidents** - Recurring or new issues that arose
5. **Recent Events** - Latest updates and current status

## 🎯 How to Use

1. **Upload File**: Click "Upload Ticket Data" and select your file
2. **Configure AI**: Enter your Gemini API key in the sidebar
3. **View Results**: Navigate through the tabs:
   - **AI Summaries**: Product-specific storytelling summaries
   - **Analytics**: Visual charts and trends
   - **Insights**: Business recommendations
   - **Export**: Download processed data and reports

## 📊 Analytics Features

- **Ticket Volume Trends** - Daily ticket counts over time
- **Product Distribution** - Pie chart of tickets by product
- **Resolution Times** - Average resolution time by product
- **Customer Activity** - Most active customers
- **Business Insights** - Automated recommendations

## ⚙️ Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_api_key_here
```

### Config Options (config.py)

- `SELECTED_COLUMNS`: Required data columns
- `VALID_CATEGORIES`: Accepted service categories
- `CATEGORY_MAPPING`: Category to product mapping
- `DATE_FORMAT`: Expected date format in data

## 🔧 Implementation Details

### Data Processing Pipeline

1. **File Reading**: Supports multiple formats (TXT/CSV/XLSX)
2. **Column Filtering**: Keeps only required columns
3. **Category Filtering**: Removes invalid service categories
4. **Date Conversion**: Converts text dates to datetime objects
5. **Product Mapping**: Maps categories to business products
6. **Data Sorting**: Orders by acceptance time

### AI Story Generation

1. **Chronological Grouping**: Divides tickets into 5 time-based sections
2. **Data Preparation**: Formats ticket data for AI processing
3. **Gemini Integration**: Uses Google's Gemini AI for narrative generation
4. **Error Handling**: Provides fallback summaries if AI fails
5. **Story Assembly**: Combines all sections into complete narratives

### Visualization Engine

- **Plotly Integration**: Interactive charts and graphs
- **Business Metrics**: Key performance indicators
- **Trend Analysis**: Time-based patterns
- **Customer Insights**: Activity and behavior patterns

## 📈 Business Value

### For Customer Service Teams
- Understand customer journey patterns
- Identify recurring issues and trends
- Track resolution performance
- Prioritize improvement areas

### For Management
- Data-driven decision making
- Resource allocation insights
- Customer satisfaction indicators
- Operational efficiency metrics

## 🛠️ Troubleshooting

### Common Issues

**"No valid tickets found"**
- Check that your data has the required columns
- Verify SERVICE_CATEGORY contains valid values (HDW, NET, KAI, KAV, GIGA, VOD, KAD)

**"AI summary unavailable"**
- Verify Gemini API key is correct
- Check internet connection
- Try using a different Gemini model

**"Error reading file"**
- Ensure file format is TXT, CSV, or XLSX
- Check that date format matches MM/DD/YYYY HH:MM
- Verify file is not corrupted

### Performance Tips

- Large files (>10,000 tickets) may take longer to process
- AI summary generation requires internet connection
- For better performance, filter data before upload

## 🔒 Security Notes

- API keys are not stored permanently
- Uploaded files are processed in memory only
- No data is sent to external services except Gemini AI for summaries

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the in-app documentation (📚 Documentation tab)
3. Verify all requirements are met

## 🔄 Version History

- **v1.0**: Initial release with core functionality
- **v1.1**: Added analytics dashboard and business insights
- **v1.2**: Enhanced UI and export features

## 📄 License

This project is provided as-is for educational and business use.