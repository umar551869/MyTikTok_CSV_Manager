# 🎵 TikTok CSV Manager

**Industrial-grade tool for TikTok Shop affiliate management and creator outreach**

A comprehensive Streamlit application designed for managing TikTok affiliate data, analyzing creator performance, calculating commissions, and streamlining outreach campaigns.

---

## ✨ Features

### 📂 File Management
- **Upload CSV/Excel**: Auto-detect headers, handle multiple formats
- **Create New**: Build datasets from scratch
- **Multi-File Merge**: Combine multiple files with smart column mapping
  - Stack (append rows) or Join (match columns)
  - Automatic deduplication
  - Handle column mismatches

### ✍️ Data Editor
- **Interactive Spreadsheet**: Edit cells, add/delete rows dynamically
- **Column Operations**: Drop, rename, filter columns
- **Row Filtering**: Filter by any column value
- **Sorting**: Sort by any column (handles numeric strings like "1.2M")

### 📦 Batch Splitter
- **Smart Chunking**: Split large files into manageable batches
- **Customizable Size**: Set rows per batch
- **Bulk Download**: Download all batches at once

### 🔍 Username Extractor
- **Smart Extraction**: PPS-anchor based extraction with regex fallback
- **High Accuracy**: Filters out common noise and false positives
- **Debug Mode**: View extraction logic for troubleshooting

### 📊 Analytics & Processing

#### Data Processing
- **Column Selection**: Choose which columns to analyze
- **Deduplication**: Remove duplicates by any column
- **Date Filtering**: Filter by month/year
- **Sorting**: Intelligent numeric and text sorting
- **Advanced Filters**:
  - GMV range ($0 - $1M+)
  - Video count range (1-1000+)
  - Text search across any column

#### Key Metrics
- **Video Counts**: Creators by video count (1-2, 3-9, 10+)
- **GMV Segmentation**: $10K-$99K, $100K-$999K, $1M+
- **Total Metrics**: Videos, Likes, Orders, GMV

#### 💵 Commission Calculator
- **Customizable Rates**: Set commission percentage (0-100%)
- **Creator Breakdown**: See commission per creator
- **Export Reports**: Download commission reports as CSV

#### Visualizations
- **Top Creators**: Bar charts by GMV or video count
- **Distributions**: Histograms for views/GMV
- **Engagement Analysis**: 
  - Engagement rate (Likes/Views)
  - Revenue efficiency (GMV/View, GMV/Order)
- **Creator Segmentation**: 
  - Star Performers (High GMV + High Views)
  - High Revenue (High GMV)
  - High Reach (High Views)
  - Emerging (Below median)

#### 🎨 Custom Chart Builder
**12 Chart Types**:
- 2D: Scatter, Line, Bar, Box, Violin, Histogram, Pie, Sunburst, Treemap
- 3D: Scatter, Line, Surface

**Features**:
- Select X, Y, Z axes
- Color and size dimensions
- Interactive hover data

#### 📥 Bulk Export
**Templates**:
- **Top Performers**: Top 50 by GMV/Views
- **High GMV Creators**: Creators with GMV ≥ $10K
- **High Engagement**: Videos with engagement ≥ 5%
- **Custom Selection**: Choose specific columns
- **All Data**: Export everything

**Formats**: CSV or Excel (.xlsx)

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone or download the repository
cd MyTikTok_CSV_Manager

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Upload Your Data
1. Go to **📂 File Manager** → **📤 Upload CSV**
2. Select your TikTok Shop export file (.csv or .xlsx)
3. Adjust header row if needed (auto-detected)
4. Click to load data

### 2. Process & Filter
1. Navigate to **📊 Analytics & Processing**
2. Select columns to keep
3. Remove duplicates (optional)
4. Apply advanced filters:
   - Set GMV range
   - Set video count range
   - Search for specific creators

### 3. Analyze Performance
- View key metrics dashboard
- Check GMV segmentation
- Review creator segments
- Analyze engagement rates

### 4. Calculate Commissions
1. Set your commission rate (%)
2. Click **Generate Commission Report**
3. View top earners
4. Download full report

### 5. Create Custom Visualizations
1. Expand **Custom Chart Builder**
2. Select chart type (2D or 3D)
3. Choose axes and dimensions
4. Generate chart

### 6. Export Data
1. Choose export template
2. Select format (CSV or Excel)
3. Preview data
4. Download

---

## 🎯 TikTok Shop Workflows

### Workflow 1: Identify Top Performers
1. Upload TikTok Shop data
2. Go to Analytics → GMV Segmentation
3. Note creators in $100K+ category
4. Use Bulk Export → "High GMV Creators"
5. Reach out for partnership

### Workflow 2: Calculate Affiliate Earnings
1. Upload sales data
2. Set commission rate (e.g., 10%)
3. Generate commission report
4. Export for accounting

### Workflow 3: Find High-Engagement Creators
1. Upload creator data
2. Check Engagement Analysis
3. Use Bulk Export → "High Engagement"
4. Target for new campaigns

### Workflow 4: Merge Monthly Reports
1. Go to File Manager → Merge Files
2. Upload multiple monthly exports
3. Choose "Stack (Append Rows)"
4. Enable deduplication by Video ID
5. Merge and analyze trends

### Workflow 5: Segment Creators for Outreach
1. Upload data
2. View Creator Segmentation chart
3. Export each segment separately:
   - Star Performers → Premium offers
   - Emerging → Growth support
   - High Reach → Brand awareness

---

## 🔧 Technical Details

### Supported Columns
The tool auto-detects these TikTok Shop columns:
- **GMV**: "Gross merchandise value (Video) ($)", "GMV", "Revenue"
- **Views**: "Video views", "VV", "Views"
- **Creator**: "Creator name", "Creator", "Username"
- **Video ID**: "Video ID", "Item ID"
- **Engagement**: "Likes", "Comments", "Shares"
- **Orders**: "Orders", "Items sold"

### Data Parsing
- Handles formatted numbers: "1.2M", "$50K", "10.5%"
- Converts to numeric for calculations
- Preserves original formatting in exports

### Cross-Browser Compatibility
- Tested on Chrome, Firefox, Safari, Edge
- Webkit prefixes for gradients and transforms
- Consistent rem-based sizing
- Fallback fonts for all systems

---

## 💡 Tips & Best Practices

1. **Large Files**: Use Batch Splitter for files >10K rows
2. **Deduplication**: Always deduplicate by Video ID or Creator Name
3. **Filters**: Apply filters before generating charts for faster performance
4. **Commission Reports**: Generate reports monthly for tracking
5. **Custom Charts**: Use 3D scatter for multi-dimensional analysis
6. **Export Templates**: Use "Top Performers" for quick outreach lists

---

## 🐛 Troubleshooting

### Headers Not Detected
- Manually adjust "Header Row Index" in upload
- Check for merged cells or empty rows

### GMV Not Showing
- Ensure column name contains "GMV", "Gross merchandise", or "Revenue"
- Check debug info in Analytics page

### Charts Not Rendering
- Ensure columns have numeric data
- Try different chart types
- Check browser console for errors

### Excel Export Fails
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Fall back to CSV export if needed

---

## 📝 Requirements

```
streamlit
pandas
plotly
openpyxl
```

---

## 👨‍💻 Developer

**Muhammad Umar Ilyas**

---

## 📄 License

This project is provided as-is for TikTok Shop affiliate management.

---

## 🔄 Version History

### v2.0 (Production Release)
- ✅ Multi-file merge capability
- ✅ Commission calculator
- ✅ Advanced filtering (GMV, video count, text)
- ✅ Bulk export templates (CSV/Excel)
- ✅ 12 chart types including 3D
- ✅ Creator segmentation
- ✅ Cross-browser CSS fixes
- ✅ Enhanced error handling

### v1.0 (Initial Release)
- Basic CSV upload/edit
- Batch splitter
- Username extractor
- Simple analytics

---

## 🚀 Future Enhancements

- [ ] API integration with TikTok Shop
- [ ] Automated email outreach
- [ ] Campaign tracking dashboard
- [ ] Predictive analytics (ML-based)
- [ ] Multi-user collaboration

---

**Built with ❤️ for TikTok Shop Affiliates**
