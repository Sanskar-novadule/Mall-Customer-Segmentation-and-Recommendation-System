import { useState } from "react";
import axios from "axios";

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
} from "lucide-react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
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


function App() {

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [result, setResult] = useState(null);


  // ==========================================================
  // FILE SELECT
  // ==========================================================

  const handleFileChange = (event) => {

    const selectedFile =
      event.target.files[0];

    setFile(selectedFile);

    setError("");

  };


  // ==========================================================
  // UPLOAD DATASET
  // ==========================================================

  const handleUpload = async () => {

    if (!file) {

      setError(
        "Please select a CSV file first."
      );

      return;

    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    try {

      const response = await axios.post(
        `${API_URL}/upload`,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      if (
        response.data.success === false
      ) {

        setError(
          response.data.error ||
          "Analysis failed."
        );

        return;

      }

      setResult(
        response.data
      );

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to connect to backend."
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

  };


  // ==========================================================
  // DASHBOARD DATA
  // ==========================================================

  const dataset =
    result?.dataset;

  const model =
    result?.model;

  const clusters =
    result?.clusters || [];

  const clusterSummary =
    result?.cluster_summary || [];

  const features =
    result?.features;


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

          <div>

            <h2>SegmaAI</h2>

            <span>
              Customer Intelligence
            </span>

          </div>

        </div>


        <nav>

          <a className="active">
            <BarChart3 size={19} />
            Dashboard
          </a>

          <a>
            <Upload size={19} />
            Upload Dataset
          </a>

          <a>
            <Database size={19} />
            Dataset Analysis
          </a>

          <a>
            <Users size={19} />
            Customer Segments
          </a>

          <a>
            <Target size={19} />
            Recommendations
          </a>

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


        {/* ==================================================
            HEADER
        ================================================== */}

        <header className="topbar">

          <div>

            <p className="eyebrow">
              AI-POWERED ANALYTICS
            </p>

            <h1>
              Customer Segmentation
            </h1>

            <p className="subtitle">
              Automatically analyze your dataset
              and discover meaningful customer segments.
            </p>

          </div>


          {result && (

            <button
              className="secondary-button"
              onClick={handleReset}
            >
              New Analysis
            </button>

          )}

        </header>


        {/* ==================================================
            UPLOAD SECTION
        ================================================== */}

        {!result && (

          <section className="upload-section">

            <div className="upload-card">

              <div className="upload-icon">

                <FileSpreadsheet
                  size={34}
                />

              </div>

              <h2>
                Upload your dataset
              </h2>

              <p>
                Upload a CSV file and our AI
                will automatically detect useful
                features and create customer segments.
              </p>


              <label
                className="file-picker"
              >

                <Upload size={20} />

                {file
                  ? file.name
                  : "Choose CSV file"}

                <input
                  type="file"
                  accept=".csv"
                  onChange={
                    handleFileChange
                  }
                />

              </label>


              {file && (

                <div className="selected-file">

                  <CheckCircle
                    size={18}
                  />

                  {file.name}

                </div>

              )}


              {error && (

                <div className="error-box">

                  <AlertCircle
                    size={18}
                  />

                  {error}

                </div>

              )}


              <button
                className="primary-button"
                onClick={handleUpload}
                disabled={loading}
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


              <div className="upload-info">

                <span>
                  CSV files only
                </span>

                <span>
                  Automatic feature detection
                </span>

                <span>
                  AI clustering
                </span>

              </div>

            </div>

          </section>

        )}


        {/* ==================================================
            DASHBOARD
        ================================================== */}

        {result && (

          <>

            {/* ==============================================
                SUCCESS
            ============================================== */}

            <div className="success-banner">

              <CheckCircle size={20} />

              <div>

                <strong>
                  Analysis completed successfully
                </strong>

                <span>
                  {result.file?.filename}
                </span>

              </div>

            </div>


            {/* ==============================================
                METRIC CARDS
            ============================================== */}

            <section className="metrics-grid">


              <MetricCard
                icon={<Users />}
                title="Total Customers"
                value={
                  dataset?.rows ?? "-"
                }
              />


              <MetricCard
                icon={<Database />}
                title="Features"
                value={
                  dataset?.columns ?? "-"
                }
              />


              <MetricCard
                icon={<Layers />}
                title="Clusters"
                value={
                  model?.best_k ?? "-"
                }
              />


              <MetricCard
                icon={<Target />}
                title="Silhouette Score"
                value={
                  model?.silhouette_score
                    ? model.silhouette_score.toFixed(3)
                    : "-"
                }
              />

            </section>


            {/* ==============================================
                CHARTS
            ============================================== */}

            <section className="charts-grid">


              {/* Cluster distribution */}

              <div className="dashboard-card">

                <div className="card-header">

                  <div>

                    <h3>
                      Customer Distribution
                    </h3>

                    <p>
                      Customers in each segment
                    </p>

                  </div>

                  <Users size={20} />

                </div>


                <div className="chart-container">

                  <ResponsiveContainer
                    width="100%"
                    height={280}
                  >

                    <BarChart
                      data={clusters}
                    >

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
                        radius={[
                          8,
                          8,
                          0,
                          0,
                        ]}
                      />

                    </BarChart>

                  </ResponsiveContainer>

                </div>

              </div>


              {/* Cluster pie */}

              <div className="dashboard-card">

                <div className="card-header">

                  <div>

                    <h3>
                      Segment Share
                    </h3>

                    <p>
                      Distribution across clusters
                    </p>

                  </div>

                  <Layers size={20} />

                </div>


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

                            <Cell
                              key={index}
                            />

                          )
                        )}

                      </Pie>

                      <Tooltip />

                    </PieChart>

                  </ResponsiveContainer>

                </div>

              </div>

            </section>


            {/* ==============================================
                MODEL DETAILS
            ============================================== */}

            <section className="two-column">


              <div className="dashboard-card">

                <div className="card-header">

                  <div>

                    <h3>
                      Model Performance
                    </h3>

                    <p>
                      Automatic model selection
                    </p>

                  </div>

                </div>


                <div className="model-details">

                  <div>
                    <span>Algorithm</span>
                    <strong>
                      {model?.algorithm}
                    </strong>
                  </div>

                  <div>
                    <span>Best K</span>
                    <strong>
                      {model?.best_k}
                    </strong>
                  </div>

                  <div>
                    <span>Silhouette</span>
                    <strong>
                      {model?.silhouette_score?.toFixed(
                        4
                      )}
                    </strong>
                  </div>

                </div>

              </div>


              <div className="dashboard-card">

                <div className="card-header">

                  <div>

                    <h3>
                      Dataset Quality
                    </h3>

                    <p>
                      Automatic data inspection
                    </p>

                  </div>

                </div>


                <div className="model-details">

                  <div>
                    <span>Missing Values</span>
                    <strong>
                      {dataset?.total_missing}
                    </strong>
                  </div>

                  <div>
                    <span>Duplicate Rows</span>
                    <strong>
                      {dataset?.duplicate_rows}
                    </strong>
                  </div>

                  <div>
                    <span>Columns</span>
                    <strong>
                      {dataset?.columns}
                    </strong>
                  </div>

                </div>

              </div>

            </section>


            {/* ==============================================
                FEATURES
            ============================================== */}

            <section className="dashboard-card">

              <div className="card-header">

                <div>

                  <h3>
                    Automatic Feature Selection
                  </h3>

                  <p>
                    Features detected and selected by the system
                  </p>

                </div>

                <Target size={20} />

              </div>


              <div className="feature-columns">

                <FeatureList
                  title="Selected Numeric"
                  items={
                    features?.selected_numeric
                    || []
                  }
                />

                <FeatureList
                  title="Selected Categorical"
                  items={
                    features?.selected_categorical
                    || []
                  }
                />

                <FeatureList
                  title="ID Columns"
                  items={
                    features?.id_columns
                    || []
                  }
                />

              </div>

            </section>


            {/* ==============================================
                CLUSTER TABLE
            ============================================== */}

            <section className="dashboard-card">

              <div className="card-header">

                <div>

                  <h3>
                    Cluster Summary
                  </h3>

                  <p>
                    Automatically generated customer segments
                  </p>

                </div>

              </div>


              <div className="table-wrapper">

                <table>

                  <thead>

                    <tr>

                      <th>
                        Cluster
                      </th>

                      <th>
                        Customers
                      </th>

                      <th>
                        Percentage
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {clusterSummary.map(
                      (cluster) => (

                        <tr
                          key={
                            cluster.cluster
                          }
                        >

                          <td>

                            <span className="cluster-badge">

                              Cluster{" "}
                              {cluster.cluster}

                            </span>

                          </td>

                          <td>
                            {cluster.customers}
                          </td>

                          <td>
                            {cluster.percentage}%
                          </td>

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            </section>

          </>

        )}

      </main>

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

        <span>
          {title}
        </span>

        <strong>
          {value}
        </strong>

      </div>

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

      <h4>
        {title}
      </h4>

      {items.length === 0 ? (

        <p className="empty">
          None detected
        </p>

      ) : (

        items.map(
          (item) => (

            <div
              className="feature-item"
              key={item}
            >

              <CheckCircle
                size={16}
              />

              {item}

            </div>

          )
        )

      )}

    </div>

  );

}


export default App;