# Nanobot Sales Agent Blueprint (Tiles / Sanitaryware)

## Scope
- Data source: `masterdata.master_product` + `masterdata.master_product_br` (+ branch/province)
- Output: Summary + Excel (5 sheets) + optional table response
- Channels: Web (primary), Telegram/Line (secondary)

---

## Base View (use as common CTE)
```sql
WITH base_sales_view AS (
  SELECT
    COUNT(aa.product_code)::INTEGER AS productall,
    SUM(CASE WHEN assortment = 'A' THEN 1 ELSE 0 END) AS iproducta,
    SUM(CASE WHEN assortment IN ('I','D') THEN 1 ELSE 0 END) AS iproducti,
    SUM(CASE WHEN assortment = 'AS' THEN 1 ELSE 0 END) AS iproductas,
    SUM(CASE WHEN assortment = 'A' AND COALESCE(cc.stock_qty,0) > 0 THEN 1 ELSE 0 END) AS istock,
    SUM(CASE WHEN assortment = 'A' AND COALESCE(cc.stock_qty,0) <= 0 THEN 1 ELSE 0 END) AS nostock,

    aa.product_code, aa.product_name, aa.assortment,
    aa.category_name, aa.group_name, aa.pattern_name, aa.design_name,
    aa.type_code, aa.type_name, aa.vendor_name, aa.unit_name,
    CASE WHEN aa.size_name IN ('60x60 portlen','60x60 granito','60x60 ceramic') THEN '60x60'
         ELSE aa.size_name END AS size_name,
    aa.color_id, aa.color_name, aa.home_name, aa.brand_name, aa.local_name,
    aa.sale_name, aa.style_name, aa.subpattern_style_name, aa.texture_name,
    aa.classes_name, aa.shades_name,
    aa.wide, aa.long, aa.high, aa.weight,
    aa.pcs_per_sqm, aa.pcs_per_box, aa.box_per_pallet, aa.pallet_per_container,
    aa.weight_per_pallet, aa.log_sync_id,
    aa.assortment_thai, aa.assortment_oem, aa.product_oem, aa.product_sale,
    aa.product_order, aa.product_keydeal, aa.product_price, aa.product_gp,
    aa.using_type_name, aa.product_abc,

    cc.br_a, cc.br_s, cc.product_ytd_gr, cc.product_gp_lm, cc.product_gp_tm,
    cc.product_gp_ty, cc.product_mtd_mom, cc.product_mtd_yoy, cc.product_stock_gr,
    cc.mos_max_as, cc.mos_level, cc.mos_after_on_board_max_as, cc.mos_after_on_board_level,
    cc.percentile_rank_percent, cc.cumulative_percentile_percent,
    cc.rv_ytd_l2y, cc.profit_ytd_l2y, cc.rv_ytd_ly, cc.profit_ytd_ly,
    cc.rv_ytd_ty, cc.profit_ytd_ty, cc.rv_ful_l2y, cc.rv_ful_ly,
    cc.rv_lm, cc.rv_tm,
    cc.stock_qty, cc.stock_sqm, cc.stock_baht,
    cc.price_th_invat_sqm, cc.pro_th_invat_sqm, cc.icost_invat_sqm,
    cc.price_th_invat, cc.pro_th_invat, cc.icost_invat,
    cc.as_full_ly_sqm, cc.as_ytd_ly_sqm, cc.as_ytd_ty_sqm, cc.as_lm_sqm, cc.as_tm_sqm,
    cc.as_ytd_ly, cc.as_ytd_ty, cc.as_lm, cc.as_tm,
    cc.max_as_12m, cc.level,
    cc.order_value, cc.ordered_value, cc.remaining_order_value,
    aa.ordered_qty AS ordered_qty_all,
    cc.ordered_qty, cc.branch_code,
    CASE WHEN cc.branch_code = 'GH-004' THEN 'คลังสินค้า (DC)'
         ELSE br.branch_name END AS branch_name,
    pr.province_name

  FROM masterdata.master_product aa
  LEFT JOIN (
    SELECT
      cc.product_code, cc.branch_code,
      SUM(cc.product_ytd_gr) AS product_ytd_gr,
      SUM(cc.product_gp_lm) AS product_gp_lm,
      SUM(cc.product_gp_tm) AS product_gp_tm,
      SUM(cc.product_gp_ty) AS product_gp_ty,
      SUM(cc.product_mtd_mom) AS product_mtd_mom,
      SUM(cc.product_mtd_yoy) AS product_mtd_yoy,
      SUM(cc.product_stock_gr) AS product_stock_gr,
      SUM(cc.br_a) AS br_a,
      SUM(cc.br_s) AS br_s,
      SUM(cc.mos_max_as) AS mos_max_as,
      SUM(cc.mos_level) AS mos_level,
      SUM(cc.mos_after_on_board_max_as) AS mos_after_on_board_max_as,
      SUM(cc.mos_after_on_board_level) AS mos_after_on_board_level,
      SUM(cc.percentile_rank_percent) AS percentile_rank_percent,
      SUM(cc.cumulative_percentile_percent) AS cumulative_percentile_percent,
      SUM(cc.rv_ytd_l2y) AS rv_ytd_l2y,
      SUM(cc.profit_ytd_l2y) AS profit_ytd_l2y,
      SUM(cc.rv_ytd_ly) AS rv_ytd_ly,
      SUM(cc.profit_ytd_ly) AS profit_ytd_ly,
      SUM(cc.rv_ytd_ty) AS rv_ytd_ty,
      SUM(cc.profit_ytd_ty) AS profit_ytd_ty,
      SUM(cc.rv_ful_l2y) AS rv_ful_l2y,
      SUM(cc.rv_ful_ly) AS rv_ful_ly,
      SUM(cc.rv_lm) AS rv_lm,
      SUM(cc.rv_tm) AS rv_tm,
      SUM(cc.stock_qty) AS stock_qty,
      SUM(cc.stock_sqm) AS stock_sqm,
      SUM(cc.stock_baht) AS stock_baht,
      SUM(cc.price_th_invat_sqm) AS price_th_invat_sqm,
      SUM(cc.pro_th_invat_sqm) AS pro_th_invat_sqm,
      SUM(cc.icost_invat_sqm) AS icost_invat_sqm,
      SUM(cc.price_th_invat) AS price_th_invat,
      SUM(cc.pro_th_invat) AS pro_th_invat,
      SUM(cc.icost_invat) AS icost_invat,
      SUM(cc.as_full_ly_sqm) AS as_full_ly_sqm,
      SUM(cc.as_ytd_ly_sqm) AS as_ytd_ly_sqm,
      SUM(cc.as_ytd_ty_sqm) AS as_ytd_ty_sqm,
      SUM(cc.as_lm_sqm) AS as_lm_sqm,
      SUM(cc.as_tm_sqm) AS as_tm_sqm,
      SUM(cc.as_ytd_ly) AS as_ytd_ly,
      SUM(cc.as_ytd_ty) AS as_ytd_ty,
      SUM(cc.as_lm) AS as_lm,
      SUM(cc.as_tm) AS as_tm,
      SUM(cc.max_as_12m) AS max_as_12m,
      SUM(cc.level) AS level,
      SUM(cc.order_value) AS order_value,
      SUM(cc.ordered_value) AS ordered_value,
      SUM(cc.remaining_order_value) AS remaining_order_value,
      SUM(cc.ordered_qty) AS ordered_qty
    FROM masterdata.master_product_br cc
    JOIN masterdata.master_product aa ON cc.product_code = aa.product_code
    WHERE aa.group_code = '09-FC01'
      AND cc.branch_code NOT IN ('GH-190','GH-205','GH-215','GH-216')
      AND aa.assortment = 'A'
    GROUP BY cc.product_code, cc.branch_code
  ) cc ON aa.product_code = cc.product_code
  LEFT JOIN masterdata.master_branch br ON cc.branch_code = br.branch_code
  LEFT JOIN masterdata.master_province pr ON br.branch_province_id = pr.province_id
  WHERE aa.group_code = '09-FC01'
    AND aa.assortment = 'A'
  GROUP BY
    aa.product_code, aa.product_name, aa.assortment,
    aa.category_name, aa.group_name, aa.pattern_name, aa.design_name,
    aa.type_code, aa.type_name, aa.vendor_name, aa.unit_name,
    CASE WHEN aa.size_name IN ('60x60 portlen','60x60 granito','60x60 ceramic') THEN '60x60'
         ELSE aa.size_name END,
    aa.color_id, aa.color_name, aa.home_name, aa.brand_name, aa.local_name,
    aa.sale_name, aa.style_name, aa.subpattern_style_name, aa.texture_name,
    aa.classes_name, aa.shades_name,
    aa.wide, aa.long, aa.high, aa.weight,
    aa.pcs_per_sqm, aa.pcs_per_box, aa.box_per_pallet, aa.pallet_per_container,
    aa.weight_per_pallet, aa.log_sync_id,
    aa.assortment_thai, aa.assortment_oem, aa.product_oem, aa.product_sale,
    aa.product_order, aa.product_keydeal, aa.product_price, aa.product_gp,
    aa.using_type_name, aa.product_abc,
    cc.br_a, cc.br_s, cc.product_ytd_gr, cc.product_gp_lm, cc.product_gp_tm,
    cc.product_gp_ty, cc.product_mtd_mom, cc.product_mtd_yoy, cc.product_stock_gr,
    cc.mos_max_as, cc.mos_level, cc.mos_after_on_board_max_as, cc.mos_after_on_board_level,
    cc.percentile_rank_percent, cc.cumulative_percentile_percent,
    cc.rv_ytd_l2y, cc.profit_ytd_l2y, cc.rv_ytd_ly, cc.profit_ytd_ly,
    cc.rv_ytd_ty, cc.profit_ytd_ty, cc.rv_ful_l2y, cc.rv_ful_ly,
    cc.rv_lm, cc.rv_tm,
    cc.stock_qty, cc.stock_sqm, cc.stock_baht,
    cc.price_th_invat_sqm, cc.pro_th_invat_sqm, cc.icost_invat_sqm,
    cc.price_th_invat, cc.pro_th_invat, cc.icost_invat,
    cc.as_full_ly_sqm, cc.as_ytd_ly_sqm, cc.as_ytd_ty_sqm, cc.as_lm_sqm, cc.as_tm_sqm,
    cc.as_ytd_ly, cc.as_ytd_ty, cc.as_lm, cc.as_tm,
    cc.max_as_12m, cc.level,
    cc.order_value, cc.ordered_value, cc.remaining_order_value,
    cc.ordered_qty, cc.branch_code, branch_name, pr.province_name
)
```

---

## Sheet Queries (5 sheets)

### 1) Overview
```sql
WITH base_sales_view AS (...) 
SELECT
  COUNT(DISTINCT product_code) AS total_sku,
  SUM(rv_ytd_ty) AS revenue_ytd,
  SUM(profit_ytd_ty) AS profit_ytd,
  SUM(rv_tm) AS revenue_tm,
  SUM(rv_lm) AS revenue_lm,
  AVG(product_gp_tm) AS avg_gp_tm
FROM base_sales_view;
```

### 2) MOS < 4 (Order List)
```sql
WITH base_sales_view AS (...)
SELECT
  product_code, product_name, size_name, color_name, shades_name,
  product_abc, product_price, product_gp_tm,
  rv_ytd_ty, profit_ytd_ty,
  stock_qty, stock_sqm,
  mos_level, level,
  ordered_qty, ordered_value, remaining_order_value
FROM base_sales_view
WHERE mos_level < 4
ORDER BY rv_ytd_ty DESC;
```

### 3) MOS < 2 (Urgent)
```sql
WITH base_sales_view AS (...)
SELECT
  product_code, size_name, color_name, shades_name,
  product_abc, product_gp_tm,
  rv_ytd_ty, mos_level, level,
  ordered_qty, remaining_order_value
FROM base_sales_view
WHERE mos_level < 2
ORDER BY mos_level ASC, rv_ytd_ty DESC;
```

### 4) Size x Shade x Color Analysis
```sql
WITH base_sales_view AS (...), total AS (
  SELECT SUM(rv_ytd_ty) AS total_rev FROM base_sales_view
)
SELECT
  size_name AS size,
  shades_name AS shade,
  color_name AS color,
  COUNT(DISTINCT product_code) AS sku,
  SUM(rv_ytd_ty) AS revenue_ytd,
  SUM(profit_ytd_ty) AS profit_ytd,
  AVG(product_gp_tm) AS gp_tm,
  (SUM(rv_ytd_ty) / NULLIF((SELECT total_rev FROM total),0)) AS share
FROM base_sales_view
GROUP BY size_name, shades_name, color_name
ORDER BY revenue_ytd DESC;
```

### 5) Full SKU List
```sql
WITH base_sales_view AS (...)
SELECT
  product_code, product_name, size_name, color_name, shades_name,
  product_abc, product_price, product_gp_tm,
  rv_ytd_ty, profit_ytd_ty, rv_ytd_ly,
  stock_qty, stock_baht,
  mos_level, level,
  ordered_qty, remaining_order_value,
  CASE
    WHEN mos_level < 2 THEN '🔴 ด่วน'
    WHEN mos_level < 4 THEN '🟡 ควรสั่ง'
    ELSE '🟢 ปกติ'
  END AS status
FROM base_sales_view
ORDER BY rv_ytd_ty DESC;
```

---

## Output Format
- Excel workbook with sheets: `Overview`, `Order_MOS_LT4`, `Urgent_MOS_LT2`, `Size_Shade_Color`, `All_SKU`
- Web response: summary + table + optional file link
- Telegram/Line: summary + Excel file

---

## Agent Skills
1. `sales_query`
   - Inputs: group_code, filters (optional)
   - Outputs: results for each sheet

2. `sales_export`
   - Builds Excel with 5 sheets

3. `sales_summary`
   - Natural-language summary (Thai) with KPI + key risks

---

## Notes
- All metrics derived from `master_product_br` (no ClickHouse fact needed)
- Can be extended to add real-time fact tables later
