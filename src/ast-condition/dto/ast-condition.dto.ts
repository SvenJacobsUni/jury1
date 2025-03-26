/**
 * Data Transfer Object für AST-Bedingungen
 */
export class AstConditionDto {
  /**
   * Der Typ der Bedingung (z.B. 'common.recursion', 'python.forLoop')
   */
  type: string;

  /**
   * Die Parameter der Bedingung
   */
  parameters: any;

  /**
   * Die Nachricht für die Bedingung
   */
  message: string;

  /**
   * Ob die Bedingung erforderlich ist
   */
  required: boolean;
}
