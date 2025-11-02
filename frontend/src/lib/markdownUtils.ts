/**
 * Markdown preprocessing utilities
 * Fixes common formatting issues from AI agents, especially table rendering
 */

/**
 * Preprocess markdown to fix common formatting issues from AI agents
 * Specifically fixes triple backticks before tables which prevents table rendering
 */
export const preprocessMarkdown = (markdown: string): string => {
  let processed = markdown;

  // Fix: Triple backticks followed by text, then table
  // Common pattern from agents: ✅ ``` Top 3-5 Market Risks:\n\nRisk | ... | ...
  // The triple backticks create a code block that prevents table rendering
  
  // Strategy: Find triple backticks followed by table content, remove backticks, convert label to heading
  
  // Pattern 1: ``` Label:\n\nTable Header | Col | ...\n (with blank line)
  processed = processed.replace(/```\s*([^\n`]+)\s*\n\s*\n?([^\n]*\|[^\n]*\|[^\n]*)\s*\n/gi, (match, label, tableLine) => {
    const columnCount = (tableLine.match(/\|/g) || []).length;
    if (columnCount >= 2 && tableLine.trim()) {
      const heading = label.trim() ? `### ${label.trim()}\n\n` : '';
      return `${heading}${tableLine}\n`;
    }
    return match;
  });

  // Pattern 2: ``` Label:\nTable Header | Col | ...\n (no blank line)
  processed = processed.replace(/```\s*([^\n`]+)\s*\n([^\n]*\|[^\n]*\|[^\n]*)\s*\n/gi, (match, label, tableLine) => {
    const columnCount = (tableLine.match(/\|/g) || []).length;
    if (columnCount >= 2 && tableLine.trim()) {
      const heading = label.trim() ? `### ${label.trim()}\n\n` : '';
      return `${heading}${tableLine}\n`;
    }
    return match;
  });

  // Pattern 3: ```\nTable Header | Col | ...\n (no label)
  processed = processed.replace(/```\s*\n\s*([^\n]*\|[^\n]*\|[^\n]*)\s*\n/gi, (match, tableLine) => {
    const columnCount = (tableLine.match(/\|/g) || []).length;
    if (columnCount >= 2 && tableLine.trim()) {
      return `${tableLine}\n`;
    }
    return match;
  });

  // Ensure proper spacing before tables (markdown tables need blank lines)
  // Only add spacing if not already present
  processed = processed.replace(/([^\n|`])\n([^\n]*\|[^\n]*\|[^\n]*)\s*\n/gi, (match, before, tableLine) => {
    const columnCount = (tableLine.match(/\|/g) || []).length;
    if (columnCount >= 2 && tableLine.trim() && !before.trim().endsWith(':')) {
      // Add blank line before table for proper markdown parsing
      return `${before}\n\n${tableLine}\n`;
    }
    return match;
  });

  return processed;
};

