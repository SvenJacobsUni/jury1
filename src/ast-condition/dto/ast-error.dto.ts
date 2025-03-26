/**
 * Data Transfer Object für AST-Fehler
 */
export class AstErrorDto {
  /**
   * Fehlermeldung
   */
  message: string;

  /**
   * Fehlercode
   */
  code: string;

  /**
   * Position des Fehlers im Code (optional)
   */
  location?: {
    line: number;
    column: number;
  };
}
