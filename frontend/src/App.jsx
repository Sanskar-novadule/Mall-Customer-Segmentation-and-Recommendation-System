import { useState } from "react";
import axios from "axios";
import Papa from "papaparse";

import {
  Upload,
  Database,
  Users,
  Layers,
  Target,
  BarChart3,
  FileSpreadsheet,
  CheckCircle,
  AlertCircle,
  Loader2,
  Search,
  Download,
  RefreshCw,
  Activity,
  Brain,
  ChevronRight,
} from "lucide-react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import "./index.css";

const API_URL = "http://127.0.0.1:8000";

// ============================================================
// RECOMMENDATION HELPERS
// ============================================================

function getClusterValue(cluster, keyword) {
  const key = Object.keys(cluster || {}).find((key) =>
    key.toLowerCase().includes(keyword.toLowerCase())
  );

  return key ? Number(cluster[key]) || 0 : 0;
}

function getSegmentRecommendation(cluster) {
  const income = getClusterValue(cluster, "annual income");
  const spending = getClusterValue(cluster, "spending score");

  if (income >= 75 && spending >= 60) {
    return {
      name: "Premium / VIP Customers",
      description:
        "High-income customers with strong purchasing engagement.",
      actions: [
        "Offer premium products and exclusive deals.",
        "Create VIP loyalty and early-access programs.",
        "Use upselling and cross-selling campaigns.",
        "Provide personalized premium experiences.",
      ],
    };
  }

  if (income >= 75 && spending < 40) {
    return {
      name: "High Income - Low Engagement",
      description:
        "Customers have strong purchasing potential but currently show lower spending activity.",
      actions: [
        "Run personalized re-engagement campaigns.",
        "Offer targeted discounts and incentives.",
        "Recommend products based on previous activity.",
        "Use limited-time offers to encourage purchases.",
      ],
    };
  }

  if (income < 60 && spending >= 60) {
    return {
      name: "High Engagement Customers",
      description:
        "Customers show strong spending activity despite having relatively lower income.",
      actions: [
        "Offer affordable bundles and value deals.",
        "Introduce loyalty rewards.",
        "Use cross-selling for frequently purchased products.",
        "Encourage repeat purchases with personalized offers.",
      ],
    };
  }

  if (income < 60 && spending < 40) {
    return {
      name: "Low Engagement Customers",
      description:
        "Customers currently show lower income and lower spending activity.",
      actions: [
        "Promote affordable products and discounts.",
        "Use low-cost promotional campaigns.",
        "Offer first-purchase and repeat-purchase incentives.",
        "Monitor this segment for changes in engagement.",
      ],
    };
  }

  return {
    name: "Regular Customers",
    description:
      "Customers show balanced income and spending behavior.",
    actions: [
      "Provide personalized product recommendations.",
      "Use loyalty and repeat-purchase campaigns.",
      "Test cross-selling and upselling opportunities.",
      "Monitor customer behavior for future segmentation.",
    ],
  };
}

// ============================================================
// APP
// ============================================================

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const [activePage, setActivePage] = useState("dashboard");

  const [selectedCluster, setSelectedCluster] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const [previewData, setPreviewData] = useState([]);
  const [previewColumns, setPreviewColumns] = useState([]);

  // ==========================================================
  // FILE SELECT + CSV PREVIEW
  // ==========================================================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a CSV file.");
      setFile(null);
      setPreviewData([]);
      setPreviewColumns([]);
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);

    setPreviewData([]);
    setPreviewColumns([]);

    Papa.parse(selectedFile, {
      header: true,
      skipEmptyLines: true,
      preview: 10,

      complete: (results) => {
        if (results.errors && results.errors.length > 0) {
          console.error("CSV Preview Errors:", results.errors);
        }

        const rows = results.data || [];

        setPreviewData(rows);

        if (rows.length > 0) {
          setPreviewColumns(Object.keys(rows[0]));
        } else {
          setPreviewColumns([]);
        }
      },

      error: (parseError) => {
        console.error("CSV parsing error:", parseError);

        setError("Unable to preview this CSV file.");
      },
    });
  };

  // ==========================================================
  // UPLOAD / ANALYZE
  // ==========================================================

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await axios.post(
        `${API_URL}/upload`,
        formData
      );

      if (response.data?.success === false) {
        setError(
          response.data?.error || "Analysis failed."
        );
        return;
      }

      setResult(response.data);

      setSelectedCluster("all");
      setSearchTerm("");

      setActivePage("dashboard");
    } catch (err) {
      console.error("Upload error:", err);

      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Unable to connect to backend. Please make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // RESET
  // ==========================================================

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError("");

    setActivePage("dashboard");

    setSelectedCluster("all");
    setSearchTerm("");

    setPreviewData([]);
    setPreviewColumns([]);
  };

  // ==========================================================
  // DOWNLOAD CSV
  // ==========================================================

  const handleDownload = () => {
    const data = result?.customer_data || [];

    if (!data.length) {
      return;
    }

    const columns = Object.keys(data[0]);

    const csvRows = [];

    csvRows.push(columns.join(","));

    data.forEach((row) => {
      csvRows.push(
        columns
          .map((column) => {
            const value = row[column];

            if (value === null || value === undefined) {
              return "";
            }

            const stringValue = String(value).replace(
              /"/g,
              '""'
            );

            return `"${stringValue}"`;
          })
          .join(",")
      );
    });

    const blob = new Blob([csvRows.join("\n")], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "segmented_customers.csv";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  // ==========================================================
  // DATA
  // ==========================================================

  const dataset = result?.dataset || {};
  const model = result?.model || {};
  const clusters = result?.clusters || [];
  const clusterSummary = result?.cluster_summary || [];
  const features = result?.features || {};
  const customerData = result?.customer_data || [];

  const allKScores = model?.all_k_scores || {};

  const kScoreData = Object.entries(allKScores).map(
    ([k, score]) => ({
      k: Number(k),
      score: Number(score),
    })
  );

  // ==========================================================
  // FILTER CUSTOMERS
  // ==========================================================

  const filteredCustomers = customerData.filter(
    (customer) => {
      const clusterMatch =
        selectedCluster === "all" ||
        String(customer.cluster) ===
          String(selectedCluster);

      const searchMatch =
        !searchTerm ||
        Object.values(customer)
          .join(" ")
          .toLowerCase()
          .includes(searchTerm.toLowerCase());

      return clusterMatch && searchMatch;
    }
  );

  // ==========================================================
  // NAVIGATION
  // ==========================================================

  const navigation = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: <BarChart3 size={19} />,
    },
    {
      id: "upload",
      label: "Upload Dataset",
      icon: <Upload size={19} />,
    },
    {
      id: "analysis",
      label: "Dataset Analysis",
      icon: <Database size={19} />,
    },
    {
      id: "segments",
      label: "Customer Segments",
      icon: <Users size={19} />,
    },
    {
      id: "recommendations",
      label: "Recommendations",
      icon: <Target size={19} />,
    },
  ];

  // ==========================================================
  // PAGE TITLES
  // ==========================================================

  const pageTitles = {
    dashboard: {
      title: "Customer Segmentation",
      subtitle:
        "AI-powered customer intelligence dashboard.",
    },

    upload: {
      title: "Upload Dataset",
      subtitle:
        "Upload a customer dataset for automatic segmentation.",
    },

    analysis: {
      title: "Dataset Analysis",
      subtitle:
        "Automatic inspection and feature analysis.",
    },

    segments: {
      title: "Customer Segments",
      subtitle:
        "Explore customers grouped by behavioral patterns.",
    },

    recommendations: {
      title: "Recommendations",
      subtitle:
        "Actionable insights generated from customer segments.",
    },
  };

  // ==========================================================
  // UI
  // ==========================================================

  return (
    <div className="app">

      {/* ====================================================
          SIDEBAR
      ==================================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            <Layers size={24} />
          </div>

          <div className="brand-text">
            <h2>SegmaAI</h2>
            <span>Customer Intelligence</span>
          </div>

        </div>

        <nav className="sidebar-nav">

          {navigation.map((item) => (
            <button
              key={item.id}
              type="button"
              className={
                activePage === item.id
                  ? "nav-item active"
                  : "nav-item"
              }
              onClick={() =>
                setActivePage(item.id)
              }
            >

              <span className="nav-icon">
                {item.icon}
              </span>

              <span className="nav-label">
                {item.label}
              </span>

              {activePage === item.id && (
                <ChevronRight
                  size={16}
                  className="nav-arrow"
                />
              )}

            </button>
          ))}

        </nav>

        <div className="sidebar-bottom">

          <div className="ai-status">

            <span className="status-dot"></span>

            AI Engine Online

          </div>

        </div>

      </aside>

      {/* ====================================================
          MAIN
      ==================================================== */}

      <main className="main-content">

        {/* HEADER */}

        <header className="topbar">

          <div>

            <p className="eyebrow">
              AI-POWERED ANALYTICS
            </p>

            <h1>
              {pageTitles[activePage].title}
            </h1>

            <p className="subtitle">
              {pageTitles[activePage].subtitle}
            </p>

          </div>

          <div className="header-actions">

            <button
              type="button"
              className="secondary-button reload-button"
              onClick={() =>
                window.location.reload()
              }
              title="Reload page"
            >
              <RefreshCw size={18} />
              Reload
            </button>

            {result && (
              <button
                type="button"
                className="secondary-button"
                onClick={handleDownload}
              >
                <Download size={18} />
                Download CSV
              </button>
            )}

            {result && (
              <button
                type="button"
                className="secondary-button"
                onClick={handleReset}
              >
                New Analysis
              </button>
            )}

          </div>

        </header>

        {/* ==================================================
            INITIAL UPLOAD
        ================================================== */}

        {!result && (
          <UploadPage
            file={file}
            error={error}
            loading={loading}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
            previewData={previewData}
            previewColumns={previewColumns}
          />
        )}

        {/* ==================================================
            DASHBOARD
        ================================================== */}

        {result && activePage === "dashboard" && (
          <DashboardPage
            result={result}
            dataset={dataset}
            model={model}
            clusters={clusters}
            clusterSummary={clusterSummary}
            features={features}
            kScoreData={kScoreData}
          />
        )}

        {/* ==================================================
            UPLOAD PAGE
        ================================================== */}

        {result && activePage === "upload" && (
          <UploadPage
            file={file}
            error={error}
            loading={loading}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
            previewData={previewData}
            previewColumns={previewColumns}
          />
        )}

        {/* ==================================================
            ANALYSIS
        ================================================== */}

        {result && activePage === "analysis" && (
          <DatasetAnalysisPage
            result={result}
            dataset={dataset}
            model={model}
            features={features}
            kScoreData={kScoreData}
          />
        )}

        {/* ==================================================
            SEGMENTS
        ================================================== */}

        {result && activePage === "segments" && (
          <CustomerSegmentsPage
            clusters={clusters}
            clusterSummary={clusterSummary}
            customerData={filteredCustomers}
            selectedCluster={selectedCluster}
            setSelectedCluster={setSelectedCluster}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
          />
        )}

        {/* ==================================================
            RECOMMENDATIONS
        ================================================== */}

        {result &&
          activePage === "recommendations" && (
            <RecommendationsPage
              clusterSummary={clusterSummary}
            />
          )}

      </main>

    </div>
  );
}

// ============================================================
// UPLOAD PAGE
// ============================================================

function UploadPage({
  file,
  error,
  loading,
  onFileChange,
  onUpload,
  previewData,
  previewColumns,
}) {
  return (
    <section className="upload-section">

      <div className="upload-card">

        <div className="upload-icon">
          <FileSpreadsheet size={34} />
        </div>

        <h2>
          Upload your dataset
        </h2>

        <p>
          Upload a CSV file and SegmaAI
          will automatically detect useful
          features, analyze your data and
          create customer segments.
        </p>

        <label className="file-picker">

          <Upload size={20} />

          {file
            ? file.name
            : "Choose CSV file"}

          <input
            type="file"
            accept=".csv,text/csv"
            onChange={onFileChange}
          />

        </label>

        {/* SELECTED FILE */}

        {file && (
          <div className="selected-file">

            <CheckCircle size={18} />

            {file.name}

          </div>
        )}

        {/* CSV PREVIEW */}

        {previewData.length > 0 && (
          <div className="csv-preview">

            <div className="csv-preview-header">

              <div>

                <h3>
                  Dataset Preview
                </h3>

                <p>
                  Showing first{" "}
                  {previewData.length} rows
                </p>

              </div>

              <span className="preview-badge">
                CSV Preview
              </span>

            </div>

            <div className="preview-table-wrapper">

              <table className="preview-table">

                <thead>

                  <tr>

                    {previewColumns.map(
                      (column) => (
                        <th key={column}>
                          {column}
                        </th>
                      )
                    )}

                  </tr>

                </thead>

                <tbody>

                  {previewData.map(
                    (row, index) => (
                      <tr key={index}>

                        {previewColumns.map(
                          (column) => (
                            <td key={column}>

                              {row[column] !==
                                undefined &&
                              row[column] !== ""
                                ? row[column]
                                : "-"}

                            </td>
                          )
                        )}

                      </tr>
                    )
                  )}

                </tbody>

              </table>

            </div>

          </div>
        )}

        {/* ERROR */}

        {error && (
          <div className="error-box">

            <AlertCircle size={18} />

            <span>{error}</span>

          </div>
        )}

        {/* UPLOAD ACTIONS */}

        <div className="upload-actions">

          <button
            type="button"
            className="primary-button"
            onClick={onUpload}
            disabled={loading || !file}
          >

            {loading ? (
              <>
                <Loader2
                  size={19}
                  className="spin"
                />

                Analyzing Dataset...
              </>
            ) : (
              <>
                <BarChart3 size={19} />

                Analyze Dataset
              </>
            )}

          </button>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              window.location.reload()
            }
          >
            <RefreshCw size={19} />
            Reload
          </button>

        </div>

        <div className="upload-info">

          <span>CSV files</span>

          <span>
            Automatic feature detection
          </span>

          <span>
            AI clustering
          </span>

        </div>

      </div>

    </section>
  );
}

// ============================================================
// DASHBOARD PAGE
// ============================================================

function DashboardPage({
  result,
  dataset,
  model,
  clusters,
  clusterSummary,
  features,
  kScoreData,
}) {
  return (
    <>

      <div className="success-banner">

        <CheckCircle size={20} />

        <div>

          <strong>
            Analysis completed successfully
          </strong>

          <span>
            {result.file?.filename || "Dataset"}
          </span>

        </div>

      </div>

      {/* METRICS */}

      <section className="metrics-grid">

        <MetricCard
          icon={<Users />}
          title="Total Customers"
          value={dataset?.rows ?? "-"}
        />

        <MetricCard
          icon={<Database />}
          title="Features"
          value={dataset?.columns ?? "-"}
        />

        <MetricCard
          icon={<Layers />}
          title="Clusters"
          value={model?.best_k ?? "-"}
        />

        <MetricCard
          icon={<Target />}
          title="Silhouette Score"
          value={
            model?.silhouette_score !== undefined
              ? Number(
                  model.silhouette_score
                ).toFixed(3)
              : "-"
          }
        />

      </section>

      {/* CHARTS */}

      <section className="charts-grid">

        <div className="dashboard-card">

          <CardHeader
            title="Customer Distribution"
            subtitle="Customers in each segment"
            icon={<Users size={20} />}
          />

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height={280}
            >

              <BarChart data={clusters}>

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="cluster"
                  tickFormatter={(value) =>
                    `Cluster ${value}`
                  }
                />

                <YAxis />

                <Tooltip />

                <Bar
                  dataKey="customer_count"
                  radius={[8, 8, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        <div className="dashboard-card">

          <CardHeader
            title="Segment Share"
            subtitle="Distribution across clusters"
            icon={<Layers size={20} />}
          />

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height={280}
            >

              <PieChart>

                <Pie
                  data={clusters}
                  dataKey="customer_count"
                  nameKey="cluster"
                  cx="50%"
                  cy="50%"
                  outerRadius={95}
                  label
                >

                  {clusters.map(
                    (_, index) => (
                      <Cell key={index} />
                    )
                  )}

                </Pie>

                <Tooltip />

              </PieChart>

            </ResponsiveContainer>

          </div>

        </div>

      </section>

      {/* K SCORE */}

      <section className="dashboard-card">

        <CardHeader
          title="K-Means Optimization"
          subtitle="Silhouette score for each tested K"
          icon={<Activity size={20} />}
        />

        <div className="chart-container">

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <LineChart data={kScoreData}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="k" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="score"
                strokeWidth={3}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </section>

      {/* MODEL + QUALITY */}

      <section className="two-column">

        <div className="dashboard-card">

          <CardHeader
            title="Model Performance"
            subtitle="Automatic model selection"
            icon={<Brain size={20} />}
          />

          <div className="model-details">

            <div>
              <span>Algorithm</span>

              <strong>
                {model?.algorithm || "-"}
              </strong>
            </div>

            <div>
              <span>Best K</span>

              <strong>
                {model?.best_k ?? "-"}
              </strong>
            </div>

            <div>
              <span>Silhouette</span>

              <strong>
                {model?.silhouette_score !==
                undefined
                  ? Number(
                      model.silhouette_score
                    ).toFixed(4)
                  : "-"}
              </strong>
            </div>

          </div>

        </div>

        <div className="dashboard-card">

          <CardHeader
            title="Dataset Quality"
            subtitle="Automatic data inspection"
            icon={<Database size={20} />}
          />

          <div className="model-details">

            <div>
              <span>Missing Values</span>

              <strong>
                {dataset?.total_missing ?? 0}
              </strong>
            </div>

            <div>
              <span>Duplicate Rows</span>

              <strong>
                {dataset?.duplicate_rows ?? 0}
              </strong>
            </div>

            <div>
              <span>Columns</span>

              <strong>
                {dataset?.columns ?? 0}
              </strong>
            </div>

          </div>

        </div>

      </section>

      {/* FEATURES */}

      <section className="dashboard-card">

        <CardHeader
          title="Automatic Feature Selection"
          subtitle="Features detected and selected by the AI pipeline"
          icon={<Target size={20} />}
        />

        <div className="feature-columns">

          <FeatureList
            title="Selected Numeric"
            items={
              features?.selected_numeric || []
            }
          />

          <FeatureList
            title="Selected Categorical"
            items={
              features?.selected_categorical ||
              []
            }
          />

          <FeatureList
            title="ID Columns"
            items={
              features?.id_columns || []
            }
          />

        </div>

      </section>

      {/* CLUSTER SUMMARY */}

      <section className="dashboard-card">

        <CardHeader
          title="Cluster Summary"
          subtitle="Automatically generated customer segments"
          icon={<Layers size={20} />}
        />

        <ClusterTable
          clusterSummary={clusterSummary}
        />

      </section>

    </>
  );
}

// ============================================================
// DATASET ANALYSIS PAGE
// ============================================================

function DatasetAnalysisPage({
  result,
  dataset,
  model,
  features,
  kScoreData,
}) {
  return (
    <>

      <section className="metrics-grid">

        <MetricCard
          icon={<Users />}
          title="Rows"
          value={dataset?.rows ?? 0}
        />

        <MetricCard
          icon={<Database />}
          title="Columns"
          value={dataset?.columns ?? 0}
        />

        <MetricCard
          icon={<AlertCircle />}
          title="Missing Values"
          value={dataset?.total_missing ?? 0}
        />

        <MetricCard
          icon={<Activity />}
          title="Duplicate Rows"
          value={dataset?.duplicate_rows ?? 0}
        />

      </section>

      <section className="two-column">

        <div className="dashboard-card">

          <CardHeader
            title="Dataset Information"
            subtitle="Uploaded file details"
            icon={
              <FileSpreadsheet size={20} />
            }
          />

          <div className="info-list">

            <InfoRow
              label="Filename"
              value={result?.file?.filename}
            />

            <InfoRow
              label="Rows"
              value={dataset?.rows}
            />

            <InfoRow
              label="Columns"
              value={dataset?.columns}
            />

            <InfoRow
              label="Missing Values"
              value={dataset?.total_missing}
            />

            <InfoRow
              label="Duplicate Rows"
              value={dataset?.duplicate_rows}
            />

          </div>

        </div>

        <div className="dashboard-card">

          <CardHeader
            title="Model Information"
            subtitle="Clustering configuration"
            icon={<Brain size={20} />}
          />

          <div className="info-list">

            <InfoRow
              label="Algorithm"
              value={model?.algorithm}
            />

            <InfoRow
              label="Best K"
              value={model?.best_k}
            />

            <InfoRow
              label="Silhouette Score"
              value={
                model?.silhouette_score !==
                undefined
                  ? Number(
                      model.silhouette_score
                    ).toFixed(4)
                  : "-"
              }
            />

          </div>

        </div>

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="K Selection Analysis"
          subtitle="How the optimal number of clusters was selected"
          icon={<Activity size={20} />}
        />

        <div className="chart-container">

          <ResponsiveContainer
            width="100%"
            height={320}
          >

            <LineChart data={kScoreData}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="k" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="score"
                strokeWidth={3}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="Detected Columns"
          subtitle="Columns found in the uploaded dataset"
          icon={<Database size={20} />}
        />

        <div className="column-grid">

          {(dataset?.column_names || []).map(
            (column) => (
              <div
                className="column-chip"
                key={column}
              >
                {column}
              </div>
            )
          )}

        </div>

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="Feature Detection"
          subtitle="How the system interpreted the dataset"
          icon={<Target size={20} />}
        />

        <div className="feature-columns">

          <FeatureList
            title="Numeric Features"
            items={features?.numeric || []}
          />

          <FeatureList
            title="Categorical Features"
            items={
              features?.categorical || []
            }
          />

          <FeatureList
            title="Selected Features"
            items={[
              ...(features?.selected_numeric ||
                []),
              ...(features?.selected_categorical ||
                []),
            ]}
          />

        </div>

      </section>

    </>
  );
}

// ============================================================
// CUSTOMER SEGMENTS PAGE
// ============================================================

function CustomerSegmentsPage({
  clusters,
  clusterSummary,
  customerData,
  selectedCluster,
  setSelectedCluster,
  searchTerm,
  setSearchTerm,
}) {
  return (
    <>

      <section className="metrics-grid">

        <MetricCard
          icon={<Layers />}
          title="Total Segments"
          value={clusters.length}
        />

        <MetricCard
          icon={<Users />}
          title="Customers Shown"
          value={customerData.length}
        />

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="Segment Explorer"
          subtitle="Filter and explore individual customer groups"
          icon={<Users size={20} />}
        />

        <div className="segment-controls">

          <select
            value={selectedCluster}
            onChange={(event) =>
              setSelectedCluster(
                event.target.value
              )
            }
          >

            <option value="all">
              All Clusters
            </option>

            {clusters.map((cluster) => (
              <option
                key={cluster.cluster}
                value={cluster.cluster}
              >
                Cluster {cluster.cluster}
              </option>
            ))}

          </select>

          <div className="search-box">

            <Search size={18} />

            <input
              type="text"
              placeholder="Search customers..."
              value={searchTerm}
              onChange={(event) =>
                setSearchTerm(
                  event.target.value
                )
              }
            />

          </div>

        </div>

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="Customer Records"
          subtitle={`${customerData.length} records`}
          icon={<Database size={20} />}
        />

        <CustomerTable
          customers={customerData}
        />

      </section>

      <section className="dashboard-card">

        <CardHeader
          title="Segment Summary"
          subtitle="Size of every customer segment"
          icon={<Layers size={20} />}
        />

        <ClusterTable
          clusterSummary={clusterSummary}
        />

      </section>

    </>
  );
}

// ============================================================
// RECOMMENDATIONS PAGE
// ============================================================

function RecommendationsPage({
  clusterSummary,
}) {
  return (
    <section className="recommendations-section">

      <div className="recommendations-header">

        <div className="recommendation-header-icon">
          <Target size={28} />
        </div>

        <div>

          <p className="eyebrow">
            AI-POWERED INSIGHTS
          </p>

          <h2>
            AI Segment Recommendations
          </h2>

          <p>
            Actionable strategies generated
            from customer income and spending
            behavior.
          </p>

        </div>

      </div>

      <div className="recommendation-grid">

        {clusterSummary.map((cluster) => {
          const recommendation =
            getSegmentRecommendation(cluster);

          const income = getClusterValue(
            cluster,
            "annual income"
          );

          const spending = getClusterValue(
            cluster,
            "spending score"
          );

          return (
            <div
              className="recommendation-card"
              key={cluster.cluster}
            >

              <div className="recommendation-card-header">

                <div>

                  <span className="cluster-badge">
                    Cluster {cluster.cluster}
                  </span>

                  <h3>
                    {recommendation.name}
                  </h3>

                </div>

                <div className="customer-count">

                  <Users size={18} />

                  <strong>
                    {cluster.customers}
                  </strong>

                  <span>
                    customers
                  </span>

                </div>

              </div>

              <div className="segment-profile">

                <h4>
                  Segment Profile
                </h4>

                <p>
                  {recommendation.description}
                </p>

                <div className="profile-stats">

                  <div className="profile-stat">

                    <span>
                      Average Annual Income
                    </span>

                    <strong>
                      {income.toFixed(2)} k$
                    </strong>

                  </div>

                  <div className="profile-stat">

                    <span>
                      Average Spending Score
                    </span>

                    <strong>
                      {spending.toFixed(2)}
                    </strong>

                  </div>

                  <div className="profile-stat">

                    <span>
                      Customer Share
                    </span>

                    <strong>
                      {cluster.percentage ?? "-"}%
                    </strong>

                  </div>

                </div>

              </div>

              <div className="suggested-actions">

                <h4>
                  Suggested Actions
                </h4>

                <div className="action-list">

                  {recommendation.actions.map(
                    (action, index) => (
                      <div
                        className="action-item"
                        key={index}
                      >

                        <CheckCircle size={17} />

                        <span>
                          {action}
                        </span>

                      </div>
                    )
                  )}

                </div>

              </div>

            </div>
          );
        })}

      </div>

    </section>
  );
}

// ============================================================
// CARD HEADER
// ============================================================

function CardHeader({
  title,
  subtitle,
  icon,
}) {
  return (
    <div className="card-header">

      <div>

        <h3>{title}</h3>

        <p>{subtitle}</p>

      </div>

      <div className="card-header-icon">
        {icon}
      </div>

    </div>
  );
}

// ============================================================
// METRIC CARD
// ============================================================

function MetricCard({
  icon,
  title,
  value,
}) {
  return (
    <div className="metric-card">

      <div className="metric-icon">
        {icon}
      </div>

      <div>

        <span>{title}</span>

        <strong>{value}</strong>

      </div>

    </div>
  );
}

// ============================================================
// INFO ROW
// ============================================================

function InfoRow({
  label,
  value,
}) {
  return (
    <div className="info-row">

      <span>{label}</span>

      <strong>
        {value ?? "-"}
      </strong>

    </div>
  );
}

// ============================================================
// FEATURE LIST
// ============================================================

function FeatureList({
  title,
  items,
}) {
  return (
    <div className="feature-box">

      <h4>{title}</h4>

      {!items || items.length === 0 ? (
        <p className="empty">
          None detected
        </p>
      ) : (
        items.map((item) => (
          <div
            className="feature-item"
            key={item}
          >

            <CheckCircle size={16} />

            {item}

          </div>
        ))
      )}

    </div>
  );
}

// ============================================================
// CLUSTER TABLE
// ============================================================

function ClusterTable({
  clusterSummary,
}) {
  if (!clusterSummary?.length) {
    return (
      <div className="empty-state">
        No cluster summary available.
      </div>
    );
  }

  return (
    <div className="table-wrapper">

      <table>

        <thead>

          <tr>

            <th>Cluster</th>

            <th>Customers</th>

            <th>Percentage</th>

          </tr>

        </thead>

        <tbody>

          {clusterSummary.map((cluster) => (
            <tr
              key={cluster.cluster}
            >

              <td>

                <span className="cluster-badge">
                  Cluster {cluster.cluster}
                </span>

              </td>

              <td>
                {cluster.customers ?? 0}
              </td>

              <td>
                {cluster.percentage ?? 0}%
              </td>

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}

// ============================================================
// CUSTOMER TABLE
// ============================================================

function CustomerTable({
  customers,
}) {
  if (!customers?.length) {
    return (
      <div className="empty-state">
        No customers found.
      </div>
    );
  }

  const columns = Object.keys(customers[0]);

  return (
    <div className="table-wrapper">

      <table>

        <thead>

          <tr>

            {columns.map((column) => (
              <th key={column}>
                {column}
              </th>
            ))}

          </tr>

        </thead>

        <tbody>

          {customers.map(
            (customer, index) => (
              <tr key={index}>

                {columns.map((column) => (
                  <td key={column}>

                    {customer[column] === null ||
                    customer[column] ===
                      undefined
                      ? "-"
                      : String(
                          customer[column]
                        )}

                  </td>
                ))}

              </tr>
            )
          )}

        </tbody>

      </table>

    </div>
  );
}

export default App;