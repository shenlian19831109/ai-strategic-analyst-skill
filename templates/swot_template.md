# SWOT 深度分析报告

## 行业概览

本报告对 {{industry}} 进行了深入的 SWOT 分析，旨在识别其内部优势与劣势，以及外部机会与威胁，为制定战略提供依据。

## 1. 优势 (Strengths)

### 内部积极因素

{{#each strengths}}
*   **{{this.description}}**
    *   **数据支撑**: {{#each this.key_data_points}} {{this}} {{/each}}
    *   **来源**: {{#each this.references}} [{{this.description}}]({{this.url}}) {{/each}}
{{/each}}

## 2. 劣势 (Weaknesses)

### 内部消极因素

{{#each weaknesses}}
*   **{{this.description}}**
    *   **数据支撑**: {{#each this.key_data_points}} {{this}} {{/each}}
    *   **来源**: {{#each this.references}} [{{this.description}}]({{this.url}}) {{/each}}
{{/each}}

## 3. 机会 (Opportunities)

### 外部积极因素

{{#each opportunities}}
*   **{{this.description}}**
    *   **数据支撑**: {{#each this.key_data_points}} {{this}} {{/each}}
    *   **来源**: {{#each this.references}} [{{this.description}}]({{this.url}}) {{/each}}
{{/each}}

## 4. 威胁 (Threats)

### 外部消极因素

{{#each threats}}
*   **{{this.description}}**
    *   **数据支撑**: {{#each this.key_data_points}} {{this}} {{/each}}
    *   **来源**: {{#each this.references}} [{{this.description}}]({{this.url}}) {{/each}}
{{/each}}

## 5. 战略启示

{{strategic_implications}}

## 数据审计

本报告阶段共采纳 {{audit_stats.adopted_facts}} 条事实，来源于 {{audit_stats.unique_sources}} 个独立数据源。

## 参考资料

{{#each references}}
*   [{{this.description}}]({{this.url}})
{{/each}}
