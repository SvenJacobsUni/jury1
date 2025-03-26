/**
 * Data Transfer Object für AST-Bedingungsergebnisse
 */
export class AstConditionResultDto {
  /**
   * Die Nachricht der Bedingung
   */
  condition: string;

  /**
   * Ob die Bedingung erfüllt wurde
   */
  passed: boolean;

  /**
   * Details zum Ergebnis (optional)
   */
  details?: string;
}
