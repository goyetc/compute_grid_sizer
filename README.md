# Compute Grid Sizing Tool
Produce estimates using the following details:
- hw tier resources required
- estimate of concurrent or max users
- host/node sizes available

## Contents
* [dev notebook] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/Untitled.ipynb)
* [cg_node_sizer.py] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/cg2_node_sizer.py)
* [Launcher] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/endpoints/launchers#/launchers/) 

## Example output
*  (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/results/node_recommendations_2.0_4.0.html) 

## Example node data, AWS:

|Instance   |vCPU*|Mem (GiB)|
|-----------|:-----:|:---------:|
|m5.xlarge  |4    |16       |
|m5.2xlarge |8    |32       |
|m5.4xlarge |16   |64       |
|m5.8xlarge |32   |128      |
|m5.12xlarge|48   |192      |
|m5.16xlarge|64   |256      |
|m5.24xlarge|96   |384      |
|c4.large   |2    |3.75     |
|c4.xlarge  |4    |7.5      |
|c4.2xlarge |8    |15       |
|c4.4xlarge |16   |30       |
|c4.8xlarge |36   |60       |
|c5.large   |2    |4        |
|c5.xlarge  |4    |8        |
|c5.2xlarge |8    |16       |
|c5.4xlarge |16   |32       |
|c5.9xlarge |36   |72       |
|c5.12xlarge|48   |96       |
|c5.18xlarge|72   |144      |
|c5.24xlarge|96   |192      |

---

## to-do
* GPU
* combo sizing (e.g., size for hw tier A and hw tier b concurrently) 
* shiny app
